"""Capture Streamlit UI screenshots and review them with a local vision model."""

from __future__ import annotations

from pathlib import Path
import time

from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor


ARTIFACT_ROOT = Path("artifacts/ui_local_vision_review")
APP_URL = "http://127.0.0.1:8503"


def main() -> None:
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    capture_screens()
    build_contact_sheet()
    run_reviews()


def capture_screens() -> None:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1600,2600")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=opts)
    wait = WebDriverWait(driver, 60)
    try:
        driver.get(APP_URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        time.sleep(4)
        driver.save_screenshot(str(ARTIFACT_ROOT / "forecast_initial.png"))

        click_text(wait, driver, "Operations Monitor")
        driver.save_screenshot(str(ARTIFACT_ROOT / "operations_monitor.png"))

        click_text(wait, driver, "Evidence")
        driver.save_screenshot(str(ARTIFACT_ROOT / "evidence.png"))
    finally:
        driver.quit()


def click_text(wait: WebDriverWait, driver: webdriver.Chrome, text: str) -> None:
    element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[normalize-space(text())='{text}']")))
    driver.execute_script("arguments[0].click();", element)
    time.sleep(3)


def build_contact_sheet() -> None:
    paths = [
        ("Forecast landing", ARTIFACT_ROOT / "forecast_initial.png"),
        ("Operations monitor", ARTIFACT_ROOT / "operations_monitor.png"),
        ("Evidence", ARTIFACT_ROOT / "evidence.png"),
    ]
    max_width = 900
    images: list[Image.Image] = []
    for title, path in paths:
        image = Image.open(path).convert("RGB")
        ratio = max_width / image.width
        resized = image.resize((max_width, int(image.height * ratio)))
        banner = Image.new("RGB", (max_width, 50), "#1f2937")
        draw = ImageDraw.Draw(banner)
        draw.text((20, 15), title, fill="white")
        framed = Image.new("RGB", (max_width, resized.height + 50), "white")
        framed.paste(banner, (0, 0))
        framed.paste(resized, (0, 50))
        images.append(framed)

    total_height = sum(image.height for image in images) + 30 * (len(images) - 1)
    canvas = Image.new("RGB", (max_width, total_height), "#eae5dc")
    y = 0
    for image in images:
        canvas.paste(image, (0, y))
        y += image.height + 30
    canvas.save(ARTIFACT_ROOT / "contact_sheet.png")


def run_reviews() -> None:
    model_id = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForImageTextToText.from_pretrained(model_id, device_map="cpu")
    image = Image.open(ARTIFACT_ROOT / "contact_sheet.png").convert("RGB")
    prompts = {
        "overview": (
            "You are a strict senior UI/UX reviewer. Review this forecasting application contact sheet. "
            "Is it commercially usable? Answer in 6 to 10 bullet points, concrete and critical."
        ),
        "layout": (
            "Focus only on visual hierarchy, layout density, readability, spacing, and navigation. "
            "Give 8 concrete bullet points about what is wrong or right."
        ),
        "operator": (
            "Focus on the operations monitor screen. Explain whether an operator can quickly understand "
            "system state and what to do next. Give 8 bullet points."
        ),
    }
    parts: list[str] = []
    for name, question in prompts.items():
        messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": question}]}]
        prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(text=prompt, images=[image], return_tensors="pt")
        with torch.inference_mode():
            generated = model.generate(**inputs, max_new_tokens=260)
        text = processor.batch_decode(generated[:, inputs["input_ids"].shape[1] :], skip_special_tokens=True)[0].strip()
        parts.append(f"## {name}\n\n{text}")

    (Path("docs") / "ui_local_vision_review.md").write_text("\n\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()
