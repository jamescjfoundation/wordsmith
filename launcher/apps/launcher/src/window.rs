// SPDX-License-Identifier: MIT OR Apache-2.0
//! The launcher's window: a bar with its name, a card for each app with a button for each thing
//! that can be done, and a bar at the foot with when the releases were read. It has no ribbon.
//!
//! The window never waits. Reading a release, asking an installed program its version and
//! installing run on threads of their own, which send what they found back ([`Event`]); the
//! window takes the answers once a frame. Every button runs a command, as in every app on the
//! shell, so the keys, the command palette and the buttons do the same thing.

use std::process::Child;
use std::sync::mpsc::{Receiver, Sender, channel};

use jcj_shell::desktop::{DesktopApp, Start};
use jcj_shell::egui::{self, Color32, RichText, Stroke, TextureHandle, Ui};
use jcj_shell::prefs::{NoPrefs, Prefs};
use jcj_shell::theme::Theme;
use jcj_shell::{About, App, Cmd, CommandInfo, Commands, Page, Shell, ShellOptions};
use serde_json::json;
use wordsmith_launcher_core::install::Target;
use wordsmith_launcher_core::{APPS, AppInfo, Client, Installed, Release, Step, Version};

use crate::{BRAND, Setup, cli};

/// The launcher's commands.
pub mod cmd {
    /// Ask GitHub for the newest release of every app.
    pub const CHECK: &str = "launcher.check";
    /// Install the app named by the parameter `app`, or update it.
    pub const INSTALL: &str = "launcher.install";
    /// Start the app named by `app`.
    pub const OPEN: &str = "launcher.open";
    /// Ask whether to remove the app named by `app`.
    pub const REMOVE: &str = "launcher.remove";
    /// Remove it, once asked.
    pub const REMOVE_NOW: &str = "launcher.removeNow";
    /// Leave it, once asked.
    pub const KEEP: &str = "launcher.keep";
    /// Open the page of the newest release of the app named by `app`.
    pub const NOTES: &str = "launcher.notes";
    /// Open the guide.
    pub const GUIDE: &str = "launcher.guide";
    /// Open the website.
    pub const WEBSITE: &str = "launcher.website";
    /// Install the update of every app that has one.
    pub const UPDATE_ALL: &str = "launcher.updateAll";
}

/// The project's site and its guide.
const WEBSITE: &str = "https://wordsmithand.ink/";
const GUIDE: &str = "https://wordsmithand.ink/wiki/";

/// The window's measures, in points.
const PAD: f32 = 20.0;
const HEADER_H: f32 = 56.0;
const FOOTER_H: f32 = 34.0;
const GAP: f32 = 14.0;
/// A card is never narrower than this; the window fits as many to a line as it has room for.
const CARD_MIN: f32 = 300.0;
const CARD_H: f32 = 250.0;
const ICON: f32 = 52.0;
const BUTTON_H: f32 = 34.0;

/// What is known of an app's newest release.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Newest {
    /// GitHub has not been asked in this run.
    NotAsked,
    /// It is being asked.
    Asking,
    /// The app has no release yet.
    Nothing,
    /// Its newest release.
    Found(Release),
    /// GitHub could not be read, and why.
    Unread(String),
}

/// One app in the list.
#[derive(Debug)]
pub struct Row {
    /// The app.
    pub app: &'static AppInfo,
    /// Whether it is installed; `None` until its program has been looked for.
    pub installed: Option<Installed>,
    /// Its newest release.
    pub newest: Newest,
    /// What is being done with it now, in words.
    pub busy: Option<String>,
    /// What went wrong the last time, in words.
    pub problem: Option<String>,
    /// Something worth saying about the last installation that did not stop it.
    pub note: Option<String>,
    /// The question "remove it?" is open.
    pub asking_to_remove: bool,
}

/// What a row offers to do.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Offer {
    /// Install the newest release.
    Install,
    /// Replace the installed version with the newest release.
    Update,
    /// Start the app.
    Open,
    /// Remove the app.
    Remove,
}

impl Row {
    fn new(app: &'static AppInfo) -> Row {
        Row { app, installed: None, newest: Newest::NotAsked, busy: None, problem: None, note: None, asking_to_remove: false }
    }

    /// What can be done with the app now, the main thing first.
    pub fn offers(&self) -> Vec<Offer> {
        if self.busy.is_some() {
            return Vec::new();
        }
        let newest = if let Newest::Found(release) = &self.newest { Some(release.version) } else { None };
        match &self.installed {
            None => Vec::new(),
            Some(Installed::No) => newest.map(|_| Offer::Install).into_iter().collect(),
            Some(Installed::Yes { version, by_launcher }) => {
                let mut offers = Vec::new();
                // A copy whose version is not known is not replaced unasked for; one that is
                // older than the newest release is offered the update.
                if newest.zip(*version).is_some_and(|(newest, have)| newest > have) {
                    offers.push(Offer::Update);
                }
                offers.push(Offer::Open);
                if *by_launcher {
                    offers.push(Offer::Remove);
                }
                offers
            }
        }
    }

    /// The short line a card shows under the app's name: what is being looked for, or when the
    /// newest release was published.
    pub fn when(&self) -> Option<String> {
        match (&self.installed, &self.newest) {
            (None, _) => Some("Looking for it on this computer…".to_owned()),
            (_, Newest::Asking) => Some("Looking for the newest release…".to_owned()),
            (_, Newest::Nothing) => Some("No release is published yet.".to_owned()),
            (_, Newest::Found(release)) => release.date.as_deref().map(|day| format!("Newest release published {day}")),
            _ => None,
        }
    }

    /// The line under the app's name: what is installed, and what the newest release is.
    pub fn status(&self) -> String {
        let said = |version: &Version| if version.is_preview() { format!("{version} (a preview)") } else { version.to_string() };
        let have = match &self.installed {
            None => return "Looking for it on this computer…".to_owned(),
            Some(Installed::No) => None,
            Some(Installed::Yes { version, .. }) => Some(*version),
        };
        let installed = match have {
            None => "Not installed.".to_owned(),
            Some(Some(version)) => format!("Version {} is installed.", said(&version)),
            Some(None) => "Installed.".to_owned(),
        };
        let newest = match &self.newest {
            Newest::NotAsked => String::new(),
            Newest::Asking => " Looking for the newest release…".to_owned(),
            Newest::Nothing => " No release is published yet.".to_owned(),
            Newest::Unread(_) => " The newest release could not be read.".to_owned(),
            Newest::Found(release) => {
                let day = release.date.as_deref().map(|day| format!(", published {day}")).unwrap_or_default();
                match have {
                    Some(Some(version)) if version >= release.version => " It is the newest.".to_owned(),
                    Some(_) => format!(" Version {} is available{day}.", said(&release.version)),
                    None => format!(" The newest is version {}{day}.", said(&release.version)),
                }
            }
        };
        format!("{installed}{newest}")
    }
}

/// What a worker thread found.
enum Event {
    Installed(usize, Installed),
    Newest(usize, Result<Option<Release>, String>),
    Step(usize, Step),
    Done(usize, &'static str, Result<(), String>),
}

/// The launcher: the list of apps and what is going on with each.
pub struct Launcher {
    ctx: egui::Context,
    client: Client,
    setup: Setup,
    /// One row for each app, in the catalog's order.
    pub rows: Vec<Row>,
    tx: Sender<Event>,
    rx: Receiver<Event>,
    /// The apps this run started, kept until they end.
    children: Vec<Child>,
    /// Look and ask by itself at the first frame (off in a test, which must not use the network).
    by_itself: bool,
    icons: Vec<Option<TextureHandle>>,
    marks: Vec<Color32>,
    /// When every app's newest release was last read.
    checked: Option<std::time::Instant>,
}

fn index_of(command: &Cmd) -> Result<usize, String> {
    let id = command.params.get("app").and_then(|app| app.as_str()).ok_or("the command names no app")?;
    APPS.iter().position(|app| app.id == id).ok_or_else(|| format!("'{id}' is not a Wordsmith app"))
}

impl Launcher {
    /// The launcher for a window that has just opened. `by_itself`: look for the installed
    /// apps at once, and ask GitHub at once when the user lets the launcher check at start.
    pub fn new(start: &mut Start<'_>, setup: Setup, by_itself: bool) -> Launcher {
        // The launcher has no document: no New, Open, Save, Export or Print page, and no row
        // above the ribbon, which names the document and says whether it is saved. It has no
        // ribbon and no status bar either: its own bars hold its few buttons and what it knows,
        // and the preferences button opens the File page.
        let options = ShellOptions {
            quick_row: false,
            ribbon: false,
            status_bar: false,
            file_pages: vec![Page::Preferences, Page::Keys, Page::About],
            ..ShellOptions::default()
        };
        start.shell_with(|shell| shell.with_options(options));
        let (tx, rx) = channel();
        let marks: std::collections::BTreeMap<String, String> = BRAND.section("launcher").unwrap_or_default();
        let marks = APPS.iter().map(|app| marks.get(app.id).and_then(|hex| jcj_shell::theme::parse_hex(hex).ok()).unwrap_or(Color32::GRAY)).collect();
        Launcher {
            ctx: start.ctx.clone(),
            client: Client::new(env!("CARGO_PKG_VERSION")),
            setup,
            rows: APPS.iter().map(Row::new).collect(),
            tx,
            rx,
            children: Vec::new(),
            by_itself,
            icons: Vec::new(),
            marks,
            checked: None,
        }
    }

    /// Run `work` on a thread of its own and wake the window when it has sent its answer.
    fn spawn(&self, work: impl FnOnce(&Sender<Event>) + Send + 'static) {
        let (tx, ctx) = (self.tx.clone(), self.ctx.clone());
        let spawned = std::thread::Builder::new().name("launcher-work".into()).spawn(move || {
            work(&tx);
            ctx.request_repaint();
        });
        if let Err(e) = spawned {
            cli::complain(format_args!("{}: a task could not be started: {e}", crate::ID));
        }
    }

    /// Look for the installed copy of app `i` and ask it its version.
    fn look(&mut self, i: usize) {
        let (Ok(places), Some(system)) = (self.setup.places.clone(), self.setup.system) else {
            if let Some(row) = self.rows.get_mut(i) {
                row.installed = Some(Installed::No);
            }
            return;
        };
        let Some(app) = APPS.get(i) else { return };
        self.spawn(move |tx| {
            let _ = tx.send(Event::Installed(i, Target { places: &places, system, app }.installed()));
        });
    }

    /// Ask GitHub for the newest release of every app that is not being asked already.
    fn check(&mut self) {
        for i in 0..self.rows.len() {
            let (Some(row), Some(app)) = (self.rows.get_mut(i), APPS.get(i)) else { continue };
            if row.newest == Newest::Asking {
                continue;
            }
            row.newest = Newest::Asking;
            let client = self.client.clone();
            self.spawn(move |tx| {
                let _ = tx.send(Event::Newest(i, client.latest(app)));
            });
        }
    }

    /// What a command needs to act on app `i`: its row free, and this run's places and system.
    fn ready(&mut self, i: usize) -> Result<(wordsmith_launcher_core::Places, wordsmith_launcher_core::System, &'static AppInfo), String> {
        let app = APPS.get(i).ok_or("there is no such app")?;
        let system = self.setup.system.ok_or("No release file of the Wordsmith apps is built for this system.")?;
        let places = self.setup.places.clone()?;
        let row = self.rows.get_mut(i).ok_or("there is no such app")?;
        if row.busy.is_some() {
            return Err(format!("{} is busy.", app.name));
        }
        row.problem = None;
        row.note = None;
        row.asking_to_remove = false;
        Ok((places, system, app))
    }

    fn install(&mut self, i: usize) -> Result<(), String> {
        let (places, system, app) = self.ready(i)?;
        let Some(Newest::Found(release)) = self.rows.get(i).map(|row| row.newest.clone()) else {
            return Err(format!("The newest release of {} is not known yet. Check for new releases first.", app.name));
        };
        if let Some(row) = self.rows.get_mut(i) {
            row.busy = Some("Starting…".to_owned());
        }
        let client = self.client.clone();
        self.spawn(move |tx| {
            let target = Target { places: &places, system, app };
            let done = target.install(&client, &release, &mut |step| {
                let _ = tx.send(Event::Step(i, step));
            });
            let _ = tx.send(Event::Done(i, "installed", done));
        });
        Ok(())
    }

    fn remove(&mut self, i: usize) -> Result<(), String> {
        let (places, system, app) = self.ready(i)?;
        if let Some(row) = self.rows.get_mut(i) {
            row.busy = Some("Removing…".to_owned());
        }
        self.spawn(move |tx| {
            let _ = tx.send(Event::Done(i, "removed", Target { places: &places, system, app }.remove()));
        });
        Ok(())
    }

    fn open(&mut self, i: usize) -> Result<(), String> {
        let (places, system, app) = self.ready(i)?;
        if let Some(child) = (Target { places: &places, system, app }).start()? {
            self.children.push(child);
        }
        Ok(())
    }

    /// Take what the worker threads sent since the last frame.
    fn take_events(&mut self, shell: &mut Shell) {
        while let Ok(event) = self.rx.try_recv() {
            match event {
                Event::Installed(i, installed) => {
                    if let Some(row) = self.rows.get_mut(i) {
                        row.installed = Some(installed);
                    }
                }
                Event::Newest(i, found) => {
                    let Some(row) = self.rows.get_mut(i) else { continue };
                    row.newest = match found {
                        Ok(Some(release)) => Newest::Found(release),
                        Ok(None) => Newest::Nothing,
                        Err(problem) => Newest::Unread(problem),
                    };
                    if self.rows.iter().all(|row| row.newest != Newest::Asking) {
                        self.checked = Some(std::time::Instant::now());
                    }
                }
                Event::Step(i, step) => {
                    let Some(row) = self.rows.get_mut(i) else { continue };
                    match step {
                        Step::Note(note) => row.note = Some(note),
                        step => row.busy = Some(cli::words_for(&step)),
                    }
                }
                Event::Done(i, what, done) => {
                    let Some(row) = self.rows.get_mut(i) else { continue };
                    row.busy = None;
                    match done {
                        Ok(()) => shell.message = format!("{} is {what}.", row.app.name),
                        Err(problem) => row.problem = Some(problem),
                    }
                    self.look(i);
                }
            }
        }
        // An app this run started and that has ended needs nothing more from the launcher.
        self.children.retain_mut(|child| !matches!(child.try_wait(), Ok(Some(_))));
    }

    fn icon(&mut self, i: usize) -> Option<TextureHandle> {
        if self.icons.is_empty() {
            // The three apps' icons, in the catalog's order, then the launcher's own.
            let pictures: [(&str, &[u8]); 4] = [
                ("wordsmith-script", include_bytes!("../../../assets/brand/wordsmith-script-icon-128.png")),
                ("wordsmith-manuscript", include_bytes!("../../../assets/brand/wordsmith-manuscript-icon-128.png")),
                ("wordsmith-book", include_bytes!("../../../assets/brand/wordsmith-book-icon-128.png")),
                (crate::ID, include_bytes!("../../../assets/brand/icon-256.png")),
            ];
            self.icons = pictures
                .iter()
                .map(|(name, png)| {
                    let (width, height, rgba) = jcj_shell::theme::brand::decode_png(png)?;
                    let size = [usize::try_from(width).ok()?, usize::try_from(height).ok()?];
                    let picture = egui::ColorImage::from_rgba_unmultiplied(size, &rgba);
                    Some(self.ctx.load_texture(*name, picture, egui::TextureOptions::LINEAR))
                })
                .collect();
        }
        self.icons.get(i).cloned().flatten()
    }

    /// The launcher's own icon, drawn in the header.
    fn own_icon(&mut self) -> Option<TextureHandle> {
        self.icon(APPS.len())
    }

    /// The apps that have an update to install.
    fn to_update(&self) -> Vec<usize> {
        (0..self.rows.len()).filter(|&i| self.rows.get(i).is_some_and(|row| row.offers().contains(&Offer::Update))).collect()
    }

    /// The bar at the top: the launcher's name, and the button to its preferences.
    fn header(&mut self, ui: &mut Ui, shell: &mut Shell, t: &Theme) {
        let icon = self.own_icon();
        ui.horizontal(|ui| {
            ui.set_min_height(HEADER_H);
            ui.add_space(PAD);
            if let Some(texture) = &icon {
                ui.add(egui::Image::new(texture).fit_to_exact_size(egui::vec2(30.0, 30.0)));
            }
            ui.add_space(6.0);
            ui.label(RichText::new("Wordsmith").size(t.type_sizes.heading - 6.0).strong().color(t.text));
            ui.add_space(10.0);
            let (rule, _) = ui.allocate_exact_size(egui::vec2(1.0, HEADER_H - 20.0), egui::Sense::hover());
            ui.painter().rect_filled(rule, 0.0, t.border);
            ui.add_space(10.0);
            ui.label(RichText::new("LAUNCHER").size(t.type_sizes.caption).color(t.text_dim).extra_letter_spacing(2.0));
            ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                ui.add_space(PAD);
                if icon_button(ui, "options", t).on_hover_text("Preferences").clicked() {
                    shell.run(Cmd::with(jcj_shell::commands::shell_ids::FILE_PAGE, json!({ "page": "preferences" })));
                }
            });
        });
    }

    /// The row under the header: look again, and update every app that has an update.
    fn toolbar(&self, ui: &mut Ui, shell: &mut Shell, t: &Theme) {
        ui.horizontal(|ui| {
            ui.set_min_height(36.0);
            let asking = self.why_disabled(cmd::CHECK);
            let check = ui.add_enabled_ui(asking.is_none(), |ui| icon_button(ui, "update", t)).inner;
            if check.on_hover_text(asking.unwrap_or_else(|| "Check for new releases (F5)".to_owned())).clicked() {
                shell.run(Cmd::new(cmd::CHECK));
            }
            ui.add_space(6.0);
            let installed = self.rows.iter().filter(|row| matches!(row.installed, Some(Installed::Yes { .. }))).count();
            ui.label(RichText::new(format!("{installed} of {} apps installed", self.rows.len())).color(t.text_dim));
            ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                let updates = self.to_update().len();
                if updates > 0 {
                    let words = if updates == 1 { "Update 1 app".to_owned() } else { format!("Update {updates} apps") };
                    if filled_button(ui, &words, t, false).clicked() {
                        shell.run(Cmd::new(cmd::UPDATE_ALL));
                    }
                }
            });
        });
    }

    /// The line above a card's name: the version, and a link to the release's notes.
    fn card_top(&self, ui: &mut Ui, shell: &mut Shell, i: usize, mark: Color32, t: &Theme) {
        let Some(row) = self.rows.get(i) else { return };
        let have = match &row.installed {
            Some(Installed::Yes { version: Some(version), .. }) => Some(*version),
            _ => None,
        };
        let newest = if let Newest::Found(release) = &row.newest { Some(release.version) } else { None };
        let mono = |text: String, color: Color32| RichText::new(text).monospace().size(t.type_sizes.caption + 0.5).color(color);
        ui.horizontal(|ui| {
            match (have, newest) {
                (Some(have), Some(newest)) if newest > have => {
                    ui.label(mono(have.to_string(), t.text_dim));
                    ui.label(mono("→".to_owned(), t.text_dim));
                    ui.label(mono(newest.to_string(), mark).strong());
                }
                (Some(have), _) => {
                    ui.label(mono(have.to_string(), mark));
                }
                (None, Some(newest)) => {
                    ui.label(mono(newest.to_string(), t.text_dim));
                }
                (None, None) => {
                    ui.label(mono("—".to_owned(), t.text_dim));
                }
            }
            ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                if matches!(row.newest, Newest::Found(_)) {
                    let notes = ui.add(
                        egui::Label::new(RichText::new("Release notes ↗").size(t.type_sizes.caption).color(t.text_dim)).sense(egui::Sense::click()),
                    );
                    if notes.on_hover_cursor(egui::CursorIcon::PointingHand).on_hover_text("What is in this release, on GitHub").clicked() {
                        shell.run(Cmd::with(cmd::NOTES, json!({ "app": row.app.id })));
                    }
                }
            });
        });
    }

    /// The card's name, two-toned as the brand writes it, and what the app is for.
    fn card_name(&mut self, ui: &mut Ui, i: usize, mark: Color32, t: &Theme) {
        let icon = self.icon(i);
        let Some(row) = self.rows.get(i) else { return };
        ui.horizontal(|ui| {
            match &icon {
                Some(texture) => ui.add(egui::Image::new(texture).fit_to_exact_size(egui::vec2(ICON, ICON))),
                None => ui.allocate_response(egui::vec2(ICON, ICON), egui::Sense::hover()),
            };
            ui.add_space(8.0);
            ui.vertical(|ui| {
                ui.add_space(4.0);
                let (first, rest) = row.app.name.split_once(' ').unwrap_or((row.app.name, ""));
                let size = t.type_sizes.title + 6.0;
                ui.horizontal(|ui| {
                    ui.spacing_mut().item_spacing.x = 0.0;
                    ui.label(RichText::new(first).size(size).strong().color(t.text));
                    if !rest.is_empty() {
                        ui.label(RichText::new(format!(" {rest}")).size(size).strong().color(mark));
                    }
                });
                ui.label(RichText::new(row.app.summary).color(t.text_dim));
            });
        });
    }

    /// What is known of the app, and what went wrong.
    fn card_words(&self, ui: &mut Ui, i: usize, t: &Theme) {
        let Some(row) = self.rows.get(i) else { return };
        let chip = match (&row.installed, row.offers().contains(&Offer::Update)) {
            (_, true) => Some(("Update available", t.accent, t.accent_soft)),
            (Some(Installed::No), _) => Some(("Not installed", t.text_dim, t.hover)),
            _ => None,
        };
        if let Some((words, color, fill)) = chip {
            egui::Frame::new().fill(fill).corner_radius(t.radius.chip).inner_margin(egui::Margin::symmetric(8, 3)).show(ui, |ui| {
                ui.label(RichText::new(words.to_uppercase()).size(t.type_sizes.caption - 1.0).color(color).extra_letter_spacing(1.0));
            });
            ui.add_space(6.0);
        }
        if row.asking_to_remove {
            ui.label(format!("Remove {}? Your documents and its settings are kept.", row.app.name));
        } else if let Some(line) = row.when() {
            // The versions are in the line above the name; the whole sentence is under the mouse.
            ui.label(RichText::new(line).color(t.text_dim)).on_hover_text(row.status());
        }
        if let Newest::Unread(why) = &row.newest {
            ui.label(RichText::new(why).color(t.danger).size(t.type_sizes.caption));
        }
        for (text, color) in [(&row.problem, t.danger), (&row.note, t.text_dim)] {
            if let Some(text) = text {
                ui.label(RichText::new(text).color(color));
            }
        }
    }

    /// The buttons at the foot of a card: the main thing, and the rest under "…".
    fn card_buttons(&self, ui: &mut Ui, shell: &mut Shell, i: usize, t: &Theme) {
        let Some(row) = self.rows.get(i) else { return };
        let with = |id: &str| Cmd::with(id, json!({ "app": row.app.id }));
        let wide = ui.available_width();
        if let Some(busy) = &row.busy {
            ui.horizontal(|ui| {
                ui.spinner();
                ui.label(busy);
            });
            return;
        }
        if row.asking_to_remove {
            ui.horizontal(|ui| {
                let half = (wide - ui.spacing().item_spacing.x) / 2.0;
                if ui.add_sized([half, BUTTON_H], outlined("Keep", t)).clicked() {
                    shell.run(with(cmd::KEEP));
                }
                if ui.add_sized([half, BUTTON_H], outlined(RichText::new("Remove").color(t.danger), t)).clicked() {
                    shell.run(with(cmd::REMOVE_NOW));
                }
            });
            return;
        }
        let offers = row.offers();
        // Open is the main thing once the app is installed; an update waits beside it.
        let main = if offers.contains(&Offer::Open) { Some(Offer::Open) } else { offers.first().copied() };
        let update = offers.contains(&Offer::Update);
        let remove = offers.contains(&Offer::Remove);
        let notes = matches!(row.newest, Newest::Found(_));
        ui.horizontal(|ui| {
            let gap = ui.spacing().item_spacing.x;
            let more = notes || remove;
            let side = BUTTON_H;
            let room = wide - if more { side + gap } else { 0.0 } - if update && main == Some(Offer::Open) { 90.0 + gap } else { 0.0 };
            match main {
                Some(Offer::Open) => {
                    if ui.add_sized([room, BUTTON_H], outlined(RichText::new("OPEN").strong().extra_letter_spacing(1.5), t)).clicked() {
                        shell.run(with(cmd::OPEN));
                    }
                }
                Some(Offer::Install | Offer::Update) => {
                    let label = if main == Some(Offer::Install) { "INSTALL" } else { "UPDATE" };
                    ui.allocate_ui(egui::vec2(room, BUTTON_H), |ui| {
                        if filled_button(ui, label, t, true).clicked() {
                            shell.run(with(cmd::INSTALL));
                        }
                    });
                }
                _ => {
                    let waiting = if row.installed.is_none() { "Looking…" } else { "Waiting for the newest release…" };
                    ui.add_sized([room, BUTTON_H], egui::Label::new(RichText::new(waiting).color(t.text_dim)));
                }
            }
            let update_words = RichText::new("UPDATE").strong().extra_letter_spacing(1.5);
            if update && main == Some(Offer::Open) && ui.add_sized([90.0, BUTTON_H], outlined(update_words, t)).clicked() {
                shell.run(with(cmd::INSTALL));
            }
            if more {
                let more = ui.add_sized([side, BUTTON_H], outlined("…", t)).on_hover_text("More");
                egui::Popup::menu(&more).show(|ui| {
                    if notes && ui.button("Release notes").clicked() {
                        shell.run(with(cmd::NOTES));
                    }
                    if remove && ui.button(RichText::new("Remove…").color(t.danger)).clicked() {
                        shell.run(with(cmd::REMOVE));
                    }
                });
            }
        });
    }

    fn card(&mut self, ui: &mut Ui, shell: &mut Shell, i: usize, width: f32, t: &Theme) {
        let mark = self.marks.get(i).copied().unwrap_or(Color32::GRAY);
        let frame = egui::Frame::new().fill(t.surface_high).stroke(Stroke::new(1.0, t.border)).corner_radius(t.radius.card);
        frame.show(ui, |ui| {
            ui.set_width(width);
            let top = ui.cursor().top();
            ui.vertical(|ui| {
                ui.spacing_mut().item_spacing.y = 4.0;
                egui::Frame::new().inner_margin(egui::Margin::symmetric(16, 10)).show(ui, |ui| self.card_top(ui, shell, i, mark, t));
                let (rule, _) = ui.allocate_exact_size(egui::vec2(width, 1.0), egui::Sense::hover());
                ui.painter().rect_filled(rule, 0.0, t.border);
                egui::Frame::new().inner_margin(egui::Margin { left: 16, right: 16, top: 14, bottom: 16 }).show(ui, |ui| {
                    self.card_name(ui, i, mark, t);
                    ui.add_space(12.0);
                    self.card_words(ui, i, t);
                    // The buttons sit at the card's foot, whatever the words above them took, so
                    // the cards of a line are one height and their buttons line up.
                    let room = top + CARD_H - 16.0 - BUTTON_H - ui.cursor().top();
                    if room > 0.0 {
                        ui.add_space(room);
                    }
                    self.card_buttons(ui, shell, i, t);
                });
            });
        });
    }

    /// The cards, as many to a line as the window has room for.
    fn grid(&mut self, ui: &mut Ui, shell: &mut Shell, t: &Theme) {
        let gap = GAP;
        let room = ui.available_width();
        let columns = (((room + gap) / (CARD_MIN + gap)).floor() as usize).clamp(1, self.rows.len().max(1));
        let width = ((room - gap * (columns as f32 - 1.0)) / columns as f32).floor();
        let count = self.rows.len();
        for first in (0..count).step_by(columns) {
            ui.horizontal_top(|ui| {
                ui.spacing_mut().item_spacing.x = gap;
                for i in first..(first + columns).min(count) {
                    self.card(ui, shell, i, width - 2.0, t);
                }
            });
            ui.add_space(gap);
        }
    }

    /// The bar at the foot: when the releases were read, where apps go, and the help links.
    fn footer(&self, ui: &mut Ui, shell: &mut Shell, t: &Theme) {
        let dim = |text: String| RichText::new(text).color(t.text_dim).size(t.type_sizes.caption).extra_letter_spacing(0.5);
        ui.horizontal(|ui| {
            ui.set_min_height(FOOTER_H);
            ui.add_space(PAD);
            let checked = match self.checked {
                _ if self.rows.iter().any(|row| row.newest == Newest::Asking) => "Checking for new releases…".to_owned(),
                None => "Not checked yet".to_owned(),
                Some(when) => match when.elapsed().as_secs() / 60 {
                    0 => "Checked just now".to_owned(),
                    1 => "Checked a minute ago".to_owned(),
                    minutes if minutes < 60 => format!("Checked {minutes} minutes ago"),
                    _ => "Checked over an hour ago".to_owned(),
                },
            };
            let place = match (&self.setup.places, self.setup.system) {
                (Err(problem), _) => {
                    ui.label(RichText::new(problem).color(t.danger).size(t.type_sizes.caption));
                    None
                }
                (Ok(_), None) => {
                    ui.label(
                        RichText::new("No release file of the Wordsmith apps is built for this system, so nothing can be installed here.")
                            .color(t.danger)
                            .size(t.type_sizes.caption),
                    );
                    None
                }
                (Ok(places), Some(system)) => Some(format!(
                    "Apps are installed for this account only, in {}, from the release files for {}. Every download comes from the app's own \
                     releases on GitHub and is checked against the release's checksums before it is opened. Nothing about you is sent.",
                    places.apps.display(),
                    system.name()
                )),
            };
            if let Some(place) = place {
                ui.label(dim(format!("{checked} · from the apps' releases on GitHub"))).on_hover_text(place);
            }
            ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                ui.add_space(PAD);
                if ui.link(dim("Website".to_owned())).clicked() {
                    shell.run(Cmd::new(cmd::WEBSITE));
                }
                ui.label(dim("·".to_owned()));
                if ui.link(dim("Guide".to_owned())).clicked() {
                    shell.run(Cmd::new(cmd::GUIDE));
                }
            });
        });
    }
}

/// A line across the window, between its bars and the cards.
fn rule(ui: &mut Ui, t: &Theme) {
    let (line, _) = ui.allocate_exact_size(egui::vec2(ui.available_width(), 1.0), egui::Sense::hover());
    ui.painter().rect_filled(line, 0.0, t.border);
}

/// A square button with one of the shell's icons in it.
fn icon_button(ui: &mut Ui, icon: &str, t: &Theme) -> egui::Response {
    let side = 32.0;
    let response = ui.add_sized([side, side], outlined("", t));
    let color = if ui.is_enabled() { t.text } else { t.text_dim };
    jcj_shell::icons::paint(ui.painter(), response.rect.shrink(8.0), icon, color, t.accent);
    response
}

/// A button drawn as an outline on the card, for everything but the one main thing.
fn outlined(text: impl Into<egui::WidgetText>, t: &Theme) -> egui::Button<'static> {
    egui::Button::new(text).fill(Color32::TRANSPARENT).stroke(Stroke::new(1.0, t.border))
}

/// A button filled with the brand's color, for the one thing a place asks for most.
fn filled_button(ui: &mut Ui, words: &str, t: &Theme, wide: bool) -> egui::Response {
    let text = RichText::new(words.to_uppercase()).strong().color(t.on_brand).extra_letter_spacing(1.5);
    let button = egui::Button::new(text).fill(t.brand).stroke(Stroke::NONE);
    if wide { ui.add_sized([ui.available_width(), BUTTON_H], button) } else { ui.add(button.min_size(egui::vec2(0.0, 32.0))) }
}

impl Commands for Launcher {
    fn command(&self, id: &str) -> Option<CommandInfo> {
        let with_app = |label: &str| Some(CommandInfo { takes_params: true, location: "Apps".into(), ..CommandInfo::new(id, label, "") });
        match id {
            cmd::INSTALL => with_app("Install or Update"),
            cmd::OPEN => with_app("Open"),
            cmd::REMOVE | cmd::REMOVE_NOW => with_app("Remove"),
            cmd::KEEP => with_app("Keep"),
            cmd::NOTES => with_app("What Is in This Release"),
            _ => self.all_commands().into_iter().find(|command| command.id == id),
        }
    }

    fn why_disabled(&self, id: &str) -> Option<String> {
        match id {
            cmd::CHECK => self.rows.iter().all(|row| row.newest == Newest::Asking).then(|| "The releases are being read.".to_owned()),
            cmd::UPDATE_ALL => self.to_update().is_empty().then(|| "Every installed app is up to date.".to_owned()),
            _ => None,
        }
    }

    fn all_commands(&self) -> Vec<CommandInfo> {
        let apps = |id: &str, label: &str, keys: &str, icon: &str| CommandInfo {
            icon: icon.into(),
            location: "Apps".into(),
            ..CommandInfo::new(id, label, keys)
        };
        vec![
            apps(cmd::CHECK, "Check for New Releases", "F5 / Mod+R", "search"),
            apps(cmd::GUIDE, "Open the Guide", "F1", "help"),
            apps(cmd::WEBSITE, "Open the Website", "", "link"),
            apps(cmd::UPDATE_ALL, "Update Every App", "", "update"),
        ]
    }
}

impl App for Launcher {
    fn document_name(&self) -> String {
        "Wordsmith apps".to_owned()
    }

    fn run(&mut self, command: &Cmd, _shell: &mut Shell) -> Result<(), String> {
        let open = |address: String| self.ctx.open_url(egui::OpenUrl::new_tab(address));
        match command.id.as_str() {
            cmd::CHECK => self.check(),
            cmd::GUIDE => open(GUIDE.to_owned()),
            cmd::WEBSITE => open(WEBSITE.to_owned()),
            cmd::INSTALL => return self.install(index_of(command)?),
            cmd::UPDATE_ALL => {
                let problems: Vec<String> = self.to_update().into_iter().filter_map(|i| self.install(i).err()).collect();
                if !problems.is_empty() {
                    return Err(problems.join(" "));
                }
            }
            cmd::OPEN => return self.open(index_of(command)?),
            cmd::REMOVE_NOW => return self.remove(index_of(command)?),
            cmd::REMOVE | cmd::KEEP => {
                let ask = command.id == cmd::REMOVE;
                if let Some(row) = self.rows.get_mut(index_of(command)?) {
                    row.asking_to_remove = ask && row.busy.is_none();
                }
            }
            cmd::NOTES => {
                let row = self.rows.get(index_of(command)?).ok_or("there is no such app")?;
                let Newest::Found(release) = &row.newest else { return Err("The newest release is not known yet.".to_owned()) };
                open(release.page(row.app));
            }
            other => return Err(format!("unknown command {other}")),
        }
        Ok(())
    }

    fn document_ui(&mut self, ui: &mut Ui, shell: &mut Shell) {
        let t = Theme::get(ui.ctx());
        ui.spacing_mut().item_spacing.y = 0.0;
        self.header(ui, shell, &t);
        rule(ui, &t);
        let body = ui.available_height() - FOOTER_H - 1.0;
        egui::ScrollArea::vertical().auto_shrink(false).max_height(body.max(0.0)).show(ui, |ui| {
            egui::Frame::new().inner_margin(egui::Margin::symmetric(PAD as i8, 14)).show(ui, |ui| {
                ui.spacing_mut().item_spacing.y = 6.0;
                self.toolbar(ui, shell, &t);
                ui.add_space(10.0);
                self.grid(ui, shell, &t);
            });
        });
        rule(ui, &t);
        self.footer(ui, shell, &t);
    }

    fn about(&self) -> About {
        About {
            summary: "Installs, updates and opens the Wordsmith apps: Wordsmith Script, Wordsmith Manuscript and Wordsmith Book. \
                      A project of The James C. J. Foundation."
                .into(),
            credit: "Based on WordCraft by the ArtCraft team.".into(),
            acknowledgments: "Built on open-source-core. Every download is read from the app's own releases on GitHub. \
                              No account, no tracking; the check for new releases can be turned off below."
                .into(),
            website: Some(WEBSITE.into()),
        }
    }
}

impl DesktopApp for Launcher {
    type Prefs = Prefs<NoPrefs>;

    fn apply_prefs(&mut self, _prefs: &NoPrefs, _shell: &mut Shell) {}

    fn prefs(&self, _last: &NoPrefs) -> NoPrefs {
        NoPrefs {}
    }

    fn tick(&mut self, _ctx: &egui::Context, shell: &mut Shell) {
        if self.by_itself {
            self.by_itself = false;
            for i in 0..self.rows.len() {
                self.look(i);
            }
            // One switch for every request the launcher makes unasked: its own update check
            // and the apps' releases. With it off, "Check Now" asks.
            if shell.updates.check_at_start {
                self.check();
            }
        }
        self.take_events(shell);
    }
}

#[cfg(test)]
mod tests {
    use std::path::PathBuf;

    use jcj_shell::desktop::Window;

    use super::*;
    use crate::DESKTOP;

    fn scratch(tag: &str) -> PathBuf {
        let dir = std::env::temp_dir().join(format!("wordsmith-launcher-window-{tag}-{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        dir
    }

    /// A window that uses neither the network nor the user's own folders.
    fn window(dir: &std::path::Path) -> (egui::Context, Window<Launcher>) {
        let ctx = egui::Context::default();
        let setup = Setup::with(Some(wordsmith_launcher_core::System::Linux), Some(dir.join("profile")), None);
        let window = Window::start(&DESKTOP, &ctx, Some(dir.join("settings")), Vec::new(), |start| Launcher::new(start, setup, false));
        (ctx, window)
    }

    fn release(version: Version) -> Newest {
        Newest::Found(Release { date: Some("2026-11-27".into()), ..Release::of(version) })
    }

    #[test]
    fn a_row_says_what_is_installed_and_offers_what_fits() {
        let mut row = Row::new(&APPS[0]);
        assert_eq!(row.status(), "Looking for it on this computer…");
        assert_eq!(row.offers(), []);
        row.installed = Some(Installed::No);
        assert_eq!(row.status(), "Not installed.");
        assert_eq!(row.offers(), [], "nothing is offered before the newest release is known");
        row.newest = release(Version::new(0, 9, 0));
        assert_eq!(row.status(), "Not installed. The newest is version 0.9.0 (a preview), published 2026-11-27.");
        assert_eq!(row.offers(), [Offer::Install]);

        row.installed = Some(Installed::Yes { version: Some(Version::new(0, 9, 0)), by_launcher: true });
        assert_eq!(row.status(), "Version 0.9.0 (a preview) is installed. It is the newest.");
        assert_eq!(row.offers(), [Offer::Open, Offer::Remove]);
        row.newest = release(Version::new(1, 0, 0));
        assert_eq!(row.status(), "Version 0.9.0 (a preview) is installed. Version 1.0.0 is available, published 2026-11-27.");
        assert_eq!(row.offers(), [Offer::Update, Offer::Open, Offer::Remove]);
        // A copy the launcher did not install is opened and updated, never removed.
        row.installed = Some(Installed::Yes { version: Some(Version::new(0, 9, 0)), by_launcher: false });
        assert_eq!(row.offers(), [Offer::Update, Offer::Open]);
        // A copy newer than the newest release (a build of one's own) is left as it is.
        row.installed = Some(Installed::Yes { version: Some(Version::new(1, 1, 0)), by_launcher: false });
        assert_eq!(row.offers(), [Offer::Open]);
        assert_eq!(row.status(), "Version 1.1.0 is installed. It is the newest.");
        // A copy that does not say its version is not replaced unasked for.
        row.installed = Some(Installed::Yes { version: None, by_launcher: false });
        assert_eq!(row.offers(), [Offer::Open]);
        assert_eq!(row.status(), "Installed. Version 1.0.0 is available, published 2026-11-27.");

        row.newest = Newest::Unread("GitHub answered 503".into());
        assert_eq!(row.status(), "Installed. The newest release could not be read.");
        row.newest = Newest::Nothing;
        assert_eq!(row.status(), "Installed. No release is published yet.");
        row.busy = Some("Downloading…".into());
        assert_eq!(row.offers(), [], "nothing is offered while something is being done");
    }

    #[test]
    fn the_window_starts_with_the_three_apps_and_no_document_pages() {
        let dir = scratch("start");
        let (_ctx, mut window) = window(&dir);
        assert_eq!(window.app.rows.iter().map(|row| row.app.id).collect::<Vec<_>>(), ["wordsmith-script", "wordsmith-manuscript", "wordsmith-book"]);
        assert_eq!(window.shell.options.file_pages, [Page::Preferences, Page::Keys, Page::About]);
        assert!(!window.shell.options.quick_row && !window.shell.options.ribbon && !window.shell.options.status_bar);
        assert_eq!(window.prefs_path(), Some(dir.join("settings").join("preferences.json").as_path()));
        // Every command the buttons and the keys reach is one the launcher has.
        for id in
            [cmd::CHECK, cmd::GUIDE, cmd::WEBSITE, cmd::UPDATE_ALL, cmd::INSTALL, cmd::OPEN, cmd::REMOVE, cmd::REMOVE_NOW, cmd::KEEP, cmd::NOTES]
        {
            assert!(window.app.command(id).is_some(), "{id}");
        }
        assert!(window.app.command("file.save").is_none());
        window.exit();
        drop(window);
        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn the_commands_act_on_the_app_they_name() {
        let dir = scratch("commands");
        let (_ctx, mut window) = window(&dir);
        let (app, shell) = (&mut window.app, &mut window.shell);
        let named = |id: &str, app: &str| Cmd::with(id, json!({ "app": app }));
        assert!(app.run(&Cmd::new(cmd::INSTALL), shell).unwrap_err().contains("names no app"));
        assert!(app.run(&named(cmd::INSTALL, "wordsmith-launcher"), shell).unwrap_err().contains("is not a Wordsmith app"));
        // Nothing is installed before the newest release is known, and nothing is started
        // that is not installed.
        assert!(app.run(&named(cmd::INSTALL, "wordsmith-book"), shell).unwrap_err().contains("not known yet"));
        assert!(app.run(&named(cmd::OPEN, "wordsmith-book"), shell).unwrap_err().contains("is not installed"));
        assert!(app.run(&named(cmd::NOTES, "wordsmith-book"), shell).is_err());
        // Removing asks first, and the question can be taken back.
        app.run(&named(cmd::REMOVE, "wordsmith-script"), shell).unwrap();
        assert!(app.rows[0].asking_to_remove && !app.rows[1].asking_to_remove);
        app.run(&named(cmd::KEEP, "wordsmith-script"), shell).unwrap();
        assert!(!app.rows[0].asking_to_remove);
        // A copy the launcher did not install is not removed: the answer comes back as the
        // row's problem, and the row is free again.
        app.run(&named(cmd::REMOVE_NOW, "wordsmith-script"), shell).unwrap();
        assert_eq!(app.rows[0].busy.as_deref(), Some("Removing…"));
        let waited = std::time::Instant::now();
        while app.rows[0].busy.is_some() && waited.elapsed() < std::time::Duration::from_secs(20) {
            app.take_events(shell);
            std::thread::sleep(std::time::Duration::from_millis(10));
        }
        assert!(app.rows[0].problem.as_deref().is_some_and(|problem| problem.contains("did not install")), "{:?}", app.rows[0]);
        assert!(app.run(&Cmd::new("launcher.nothing"), shell).is_err());
        window.exit();
        drop(window);
        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn the_window_draws_every_state_of_a_row() {
        let dir = scratch("draw");
        let (ctx, mut window) = window(&dir);
        let rows = &mut window.app.rows;
        rows[0].installed = Some(Installed::Yes { version: Some(Version::new(0, 9, 0)), by_launcher: true });
        rows[0].newest = release(Version::new(1, 0, 0));
        rows[1].installed = Some(Installed::No);
        rows[1].newest = release(Version::new(0, 9, 0));
        rows[1].busy = Some("Downloading… 25 of 50 MB".into());
        rows[2].installed = Some(Installed::Yes { version: Some(Version::new(0, 9, 0)), by_launcher: true });
        rows[2].newest = Newest::Unread("the releases of Wordsmith Book: GitHub answered 503".into());
        rows[2].problem = Some("Wordsmith Book is running. Close it and try again.".into());
        rows[2].asking_to_remove = true;
        let picture = jcj_shell::snapshot::render(&ctx, egui::vec2(820.0, 660.0), 1.0, Vec::new(), 3, |ui| window.ui_offscreen(ui));
        // Something was painted where the cards are: the picture is not one flat color.
        let (first, mut differs) = (picture.at(10, 10), false);
        for y in (200..600).step_by(20) {
            for x in (40..780).step_by(20) {
                differs |= picture.at(x, y) != first;
            }
        }
        assert!(differs, "the window drew nothing");
        window.exit();
        drop(window);
        let _ = std::fs::remove_dir_all(&dir);
    }
}
