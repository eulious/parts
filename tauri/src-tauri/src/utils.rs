use std::path::PathBuf;
use tauri::api::path::data_dir;

const IDENTIFIER: &str = "tplayer";

pub fn data_path() -> PathBuf {
    let mut resource_path = data_dir().unwrap();
    resource_path.push("Tauri");
    resource_path.push(IDENTIFIER);
    resource_path
}
