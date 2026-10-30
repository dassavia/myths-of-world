"""The Codex of Myths as a Patchouli book, built from the chapters (data/mythsofworlds/journal/codex.json, written by
gen_codex.py), the journal volumes (data/mythsofworlds/journal/<volume>.json) and their texts in the lang files.

Writes:
* data/mythsofworlds/patchouli_books/codex/book.json: the book, shown by our own Codex item;
* assets/mythsofworlds/patchouli_books/codex/<lang>/: a category per world, a sub-category per kind of entry
  (introduction, creatures, places, bosses), an entry per journal entry, in Russian and English;
* data/mythsofworlds/advancement/codex/: hidden advancements that lock the entries. The mod grants them (Progress,
  JournalEvents): codex/entry/<entry> when a creature is met or a place found, codex/chapter/<world> when the path
  reaches the world, codex/milestone/<step> for each step of the path. In creative mode the player has all of them.

Run after gen_codex.py.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_greek_assets import NS, assets, data, write_json  # noqa: E402

BOOK = "codex"
LANGS = ("ru_ru", "en_us")
KINDS = ["intro", "creature", "place", "boss"]
KIND_ICONS = {"intro": "minecraft:writable_book", "creature": "minecraft:spider_eye", "place": "minecraft:compass",
              "boss": "minecraft:wither_skeleton_skull"}
TEXT = {
    "landing": ("Здесь записано всё, что вы узнали о мире мифов. Встречайте существ, побеждайте чудовищ и находите "
                "места, и страницы откроются сами.$(br2)Главы миров открываются по мере прохождения пути героя. "
                "В творческом режиме открыто всё.",
                "Everything you have learned of the world of myths is written here. Meet creatures, defeat monsters "
                "and find places, and the pages open by themselves.$(br2)The chapters of the worlds open as you walk "
                "the hero's path. In creative mode everything is open."),
    "map": ("Путь мира", "Path of the World"),
    "map_intro": ("Шаги этого мира по порядку. Каждый открывает новые страницы.",
                  "The steps of this world in order. Each one opens new pages."),
    "requires": ("Глава откроется, когда: ", "The chapter opens when: "),
}


def lang(code):
    with open(assets("lang", f"{code}.json"), encoding="utf-8") as f:
        return json.load(f)


def adv_id(kind, name):
    return f"{NS}:codex/{kind}/{name.replace('.', '_')}"


def advancement(kind, name):
    """A hidden advancement with no display that only the mod grants."""
    write_json(data("advancement", "codex", kind, name.replace(".", "_") + ".json"),
               {"criteria": {"granted": {"trigger": "minecraft:impossible"}}})


def text(value):
    """Lang text to Patchouli markup: line breaks become $(br)."""
    return value.replace("$", "").replace("\n", "$(br)")


def main():
    with open(data("journal", "codex.json"), encoding="utf-8") as f:
        chapters = json.load(f)["chapters"]
    langs = {code: lang(code) for code in LANGS}
    index = LANGS.index

    write_json(data("patchouli_books", BOOK, "book.json"), {
        "name": f"item.{NS}.codex",
        "landing_text": f"book.{NS}.codex.landing",
        "version": 1,
        "use_resource_pack": True,
        "i18n": True,
        "custom_book_item": f"{NS}:codex",
        "dont_generate_book": True,
        "show_progress": True,
        "book_texture": "patchouli:textures/gui/book_brown.png",
        "text_overflow_mode": "resize",
        "pause_game": False,
    })
    for code in LANGS:
        path = assets("lang", f"{code}.json")
        langs[code][f"book.{NS}.codex.landing"] = TEXT["landing"][index(code)]
        write_json(path, langs[code])

    root = assets("patchouli_books", BOOK)
    for code in LANGS:
        for sub in ("categories", "entries"):
            folder = os.path.join(root, code, sub)
            if os.path.isdir(folder):
                for dirpath, _, files in os.walk(folder):
                    for name in files:
                        os.remove(os.path.join(dirpath, name))

    milestones = set()
    for number, chapter in enumerate(chapters):
        cid = chapter["id"]
        with open(data("journal", f"{chapter['volume']}.json"), encoding="utf-8") as f:
            entries = json.load(f)["entries"]
        if chapter["requires"]:
            advancement("chapter", cid)
        chapter_lock = adv_id("chapter", cid) if chapter["requires"] else None
        for step in chapter["steps"]:
            milestones.add(step["milestone"])
        for code in LANGS:
            tr = langs[code]
            i = index(code)
            desc = tr.get(f"journal.{NS}.{chapter['volume']}.intro", "")
            if chapter["requires"]:
                needs = ", ".join(tr[f"codex.{NS}.milestone.{m}"] for m in chapter["requires"])
                desc = (desc + "$(br2)" if desc else "") + TEXT["requires"][i] + needs
            write_json(os.path.join(root, code, "categories", f"{cid}.json"), {
                "name": tr[f"codex.{NS}.chapter.{cid}"], "description": text(desc),
                "icon": chapter["icon"], "sortnum": number})
            kinds = [k for k in KINDS if any(e["category"] == k for e in entries)]
            for k_number, kind in enumerate(kinds):
                write_json(os.path.join(root, code, "categories", f"{cid}_{kind}.json"), {
                    "name": tr[f"journal.{NS}.category.{kind}"], "description": "",
                    "icon": KIND_ICONS[kind], "parent": f"{NS}:{cid}", "sortnum": k_number})
            if chapter["steps"]:
                steps = "".join(f"$(li){tr[f'codex.{NS}.milestone.{s['milestone']}']}" for s in chapter["steps"])
                entry = {"name": TEXT["map"][i], "icon": chapter["icon"], "category": f"{NS}:{cid}", "priority": True,
                         "sortnum": -1, "pages": [{"type": "patchouli:text", "text": TEXT["map_intro"][i] + "$(br)" + steps}]}
                if chapter_lock:
                    entry["advancement"] = chapter_lock
                write_json(os.path.join(root, code, "entries", cid, "path.json"), entry)
            for e_number, e in enumerate(entries):
                key = f"journal.{NS}.{e['id']}"
                pages = []
                if "entity" in e:
                    pages.append({"type": "patchouli:entity", "entity": e["entity"], "name": tr[key + ".title"]})
                for page in range(1, e["pages"] + 1):
                    pages.append({"type": "patchouli:text", "text": text(tr[f"{key}.page{page}"])})
                entry = {"name": tr[key + ".title"], "icon": chapter["icon"], "category": f"{NS}:{cid}_{e['category']}",
                         "sortnum": e_number, "pages": pages}
                if "entity" in e or "structure" in e:
                    entry["advancement"] = adv_id("entry", e["id"])
                    if code == LANGS[0]:
                        advancement("entry", e["id"])
                elif chapter_lock:
                    entry["advancement"] = chapter_lock
                write_json(os.path.join(root, code, "entries", cid, e["id"].split(".", 1)[1] + ".json"), entry)
    for milestone in sorted(milestones):
        advancement("milestone", milestone)
    print(f"book: {len(chapters)} chapters, {len(milestones)} milestones")


if __name__ == "__main__":
    main()
