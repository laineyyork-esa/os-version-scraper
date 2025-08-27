def compile_os_updates():
    print("🧪 Using dummy data...")
    data = [{
        "Platform": "TestOS",
        "Current Live OS": "1.0",
        "Available Beta Release": "2.0 beta 1",
        "Available Beta Date": "27-Aug-25",
        "Major Release": "2",
        "Major Release Date": "27-Aug-25"
    }]
    df = pd.DataFrame(data)
    df["Scraped At"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv("latest_os_versions.csv", index=False)
    print("✅ Dummy CSV written.")
