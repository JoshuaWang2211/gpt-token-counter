import tiktoken, os

SUPPORTED_MODELS = [
    "gpt-4o", "gpt-4o-mini",
    "gpt-4", "gpt-4-turbo",
    "gpt-3.5-turbo",
    "text-davinci-003", "text-davinci-002",
    "text-embedding-ada-002",
    "davinci", "curie", "babbage", "ada",
    "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano",
]

DISALLOW_EXTS = {".docx", ".xlsx", ".pdf"}

def count_tokens(text, model):
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def get_multiline_input(prompt="請貼上多行內容，輸入 x 後按 Enter 結束："):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip() == "x":
            break
        lines.append(line)
    return "\n".join(lines)

VERSION = "v1.0.0 (2025-06-19)"

def interactive():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"🧮 GPT Token 計算器 - {VERSION}\n")
    print("📌 注意：支援模型清單依 2025 年 6 月為準，未來模型更新請留意新版\n")
    print("📌 使用說明\n")
    print("1️⃣ 輸入方式：")
    print("   - 單行文字：直接輸入文字後按 Enter")
    print("   - 多行文字：用於貼上多行或多段文章，輸入 /multi，結束請輸入 x 後按 Enter")
    print("   - 檔案內容：輸入檔案完整路徑，例如 ./file.txt。如檔案在同一個資料夾中，可直接輸入檔案名")
    print("  ⚠️ 僅支援純文字檔案，不支援 .docx、.xlsx、.pdf 等檔案\n")
    print("2️⃣ 可用指令：")
    print("   - /model [模型名稱]    切換模型 (例如：/model gpt-4.1)")
    print("   - /list                列出支援模型")
    print("   - /multi               多行輸入\n")
    print("3️⃣ 結束本程式請直接按 Enter\n")

    model = "gpt-4o"
    print(f"👉 當前模型：{model}\n")

    while True:
        inp = input("輸入文字 / 檔案 / 命令：").strip()
        if not inp:
            break

        # 指令：列出模型
        if inp.lower() == "/list":
            print("📋 支援模型如下：")
            print(", ".join(SUPPORTED_MODELS), "\n")
            continue

        # 指令：切換模型
        if inp.lower().startswith("/model"):
            parts = inp.split()
            if len(parts) == 2:
                cmd = parts[1]
                if cmd in SUPPORTED_MODELS:
                    model = cmd
                    print(f"✅ 模型已切換為：{model}\n")
                else:
                    print(f"❌ 不支援：{cmd}")
                    print("📌 可用模型請用 /list 查看\n")
            else:
                print("⚠️ 請輸入 `/model 模型名稱`\n")
            continue

        # 多行輸入模式
        elif inp.lower() == "/multi":
            text = get_multiline_input()
            src = "[多行輸入]"

        # 檔案判斷
        elif os.path.exists(inp):
            ext = os.path.splitext(inp)[1].lower()
            if ext in DISALLOW_EXTS:
                print("❌ 不支援該檔案類型（純文字以外請先轉檔）\n")
                continue
            try:
                with open(inp, encoding='utf-8') as f:
                    text = f.read()
                src = f"[檔案]{inp}"
            except Exception as e:
                print(f"❌ 讀取檔案失敗：{e}\n")
                continue

        # 文字判斷
        else:
            if "\n" in inp or "\\n" in inp:
                if "\\n" in inp:
                    text = inp.replace("\\n", "\n")
                else:
                    text = inp
                src = "[多行文字]"
            else:
                text = inp
                src = "[單行文字]"

        cnt = count_tokens(text, model)
        print(f"✅ 來源：{src} | 模型：{model} | Token 數：{cnt}\n")

    input("👋 按 Enter 關閉")

if __name__ == "__main__":
    interactive()
