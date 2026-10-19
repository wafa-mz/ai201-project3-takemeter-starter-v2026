from pathlib import Path

import requests
import pandas as pd

url = "https://www.reddit.com/r/truegaming/top.json"
headers = {"User-Agent": "TakeMeter student project post collector"}
target_total = 200
existing_texts = set()

if Path("labels.csv").exists():
    existing_df = pd.read_csv("labels.csv")
    if "text" not in existing_df.columns:
        raise ValueError("labels.csv must have a 'text' column.")
    existing_texts = set(existing_df["text"].dropna().astype(str))

target_posts = max(0, target_total - len(existing_texts))
print(f"Fetching up to {target_posts} new posts from r/TrueGaming...")

posts = []
seen_ids = set()
seen_texts = set(existing_texts)
after = None

while len(posts) < target_posts:
    params = {"t": "all", "limit": 100}
    if after:
        params["after"] = after

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    listing = data.get("data", {})

    for child in listing.get("children", []):
        post = child.get("data", {})
        post_id = post.get("id")
        body = post.get("selftext", "")
        if (
            post.get("stickied")
            or not post_id
            or post_id in seen_ids
            or not body
            or body in ("[deleted]", "[removed]")
        ):
            continue

        title = post.get("title", "").strip()
        text = f"{title}\n\n{body}".strip()
        if text and text not in seen_texts:
            posts.append({"text": text, "label": "", "note": ""})
            seen_ids.add(post_id)
            seen_texts.add(text)
            if len(posts) == target_posts:
                break

    after = listing.get("after")
    if not after:
        break

df = pd.DataFrame(posts, columns=["text", "label", "note"])
df.to_csv("fetched_posts.csv", index=False)
print(f"Saved {len(posts)} posts to fetched_posts.csv.")
print("The label and note columns are intentionally blank; label each post before")
print("copying the finished rows into labels.csv.")
if target_posts == 0:
    print(f"labels.csv already has at least {target_total} text rows.")
elif len(posts) < target_posts:
    print(
        f"Only {len(posts)} new posts were available from the requested listing; "
        f"collect {target_posts - len(posts)} more manually."
    )