for item in items:
    title = item.find("title")

    if title is None:
        continue

    text = title.text

    if "Berikut adalah member yang akan tampil" in text:
        print("=" * 80)
        print(text)
        print()
