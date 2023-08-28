#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

mod utils;
use std::fs::{create_dir_all, read_to_string, File};
use std::io::Write;

const STATUS_OK: &str = "{'status': 'ok'}";

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            init,
            mkdir,
            writefile,
            readfile,
            set,
            get,
            get_request
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[tauri::command]
async fn get_request() -> Result<String, &'static str> {
    // let body = match reqwest::get("http://httpbin.org/get").await?.text().await?;
    let response = reqwest::get("http://httpbin.org/geta").await.unwrap();
    let body = response.text().await.unwrap();
    println!("Body: {:?}", body);
    Ok(body)
}

#[tauri::command]
fn init<'a>() -> Result<&'a str, &'a str> {
    create_dir_all(utils::data_path()).unwrap();
    Ok(STATUS_OK)
}

#[tauri::command]
fn mkdir(path: &str) -> Result<&str, &str> {
    create_dir_all(path).unwrap();
    Ok(STATUS_OK)
}

#[tauri::command]
fn writefile<'a>(path: &'a str, text: &'a str) -> Result<&'a str, &'a str> {
    let mut file = File::create(&path).unwrap();
    file.write_all(text.as_bytes()).unwrap();
    file.flush().unwrap();
    Ok(STATUS_OK)
}

#[tauri::command]
fn readfile(path: &str) -> Result<String, &str> {
    let text = read_to_string(&path).unwrap();
    Ok(text)
}

#[tauri::command]
fn set<'a>(key: &'a str, value: &'a str) -> Result<&'a str, &'a str> {
    let db_path = utils::data_path();
    let db = sled::open(db_path).unwrap();
    db.insert(key.as_bytes(), value.as_bytes()).unwrap();
    Ok(value)
}

#[tauri::command]
fn get(key: &str) -> Result<String, &str> {
    let db_path = utils::data_path();
    let db = sled::open(db_path).unwrap();
    match db.get(key.as_bytes()).unwrap() {
        None => Err("not found"),
        Some(res) => Ok(String::from_utf8(res.to_vec()).unwrap()),
    }
}
