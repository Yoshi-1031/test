"""Script to generate a PowerPoint presentation from the master thesis example."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# --- Color scheme ---
COLOR_PRIMARY = RGBColor(0x1B, 0x3A, 0x5C)    # Dark navy
COLOR_ACCENT = RGBColor(0x2E, 0x86, 0xC1)     # Blue accent
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_LIGHT_BG = RGBColor(0xF0, 0xF4, 0xF8)
COLOR_TEXT = RGBColor(0x2C, 0x3E, 0x50)
COLOR_SUBTITLE = RGBColor(0x5D, 0x6D, 0x7E)


def add_background(slide, color):
    """Set slide background color."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, left, top, width, height, color):
    """Add a colored rectangle shape."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_textbox(slide, left, top, width, height, text, font_size=18,
                bold=False, color=COLOR_TEXT, alignment=PP_ALIGN.LEFT, font_name="Meiryo"):
    """Add a textbox with specified formatting."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_bullet_slide(slide, items, left, top, width, height, font_size=16,
                     color=COLOR_TEXT, font_name="Meiryo"):
    """Add a textbox with bullet points."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = font_name
        p.space_after = Pt(8)
        p.level = 0
    return txBox


def add_section_header(slide):
    """Add a colored bar at the top for section slides."""
    add_shape(slide, Inches(0), Inches(0), prs.slide_width, Inches(0.08), COLOR_ACCENT)


def create_title_slide():
    """Slide 1: Title slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    add_background(slide, COLOR_PRIMARY)

    # Decorative accent bar
    add_shape(slide, Inches(1.5), Inches(2.2), Inches(1.0), Inches(0.06), COLOR_ACCENT)

    # Title
    add_textbox(slide, Inches(1.5), Inches(2.5), Inches(10), Inches(1.5),
                "ソーシャルメディアの利用が\n若者のメンタルヘルスに与える影響について",
                font_size=36, bold=True, color=COLOR_WHITE)

    # Author & date
    add_textbox(slide, Inches(1.5), Inches(4.5), Inches(6), Inches(0.5),
                "後藤 潤", font_size=20, color=RGBColor(0xAE, 0xBF, 0xD5))
    add_textbox(slide, Inches(1.5), Inches(5.1), Inches(6), Inches(0.5),
                "2024年8月21日", font_size=16, color=RGBColor(0x85, 0x99, 0xAD))


def create_agenda_slide():
    """Slide 2: Agenda / Table of Contents."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, COLOR_WHITE)
    add_section_header(slide)

    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(6), Inches(0.8),
                "目次", font_size=32, bold=True, color=COLOR_PRIMARY)

    sections = [
        "1. はじめに — 研究の背景・目的・文献レビュー",
        "2. データ — 使用データ・変数定義・前処理",
        "3. 実証モデルと分析手法 — 仮説・モデル・手法",
        "4. 結果 — 主要結果・ロバスト性検証・政策的含意",
        "5. 結論 — 要約・貢献・今後の課題・政策提言",
    ]
    add_bullet_slide(slide, sections, Inches(1.2), Inches(1.8), Inches(10), Inches(4.5),
                     font_size=20, color=COLOR_TEXT)


def create_intro_slide():
    """Slide 3: Introduction."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, COLOR_WHITE)
    add_section_header(slide)

    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(10), Inches(0.8),
                "1. はじめに", font_size=32, bold=True, color=COLOR_PRIMARY)

    # Left column
    add_shape(slide, Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8), COLOR_LIGHT_BG)
    add_textbox(slide, Inches(1.1), Inches(2.0), Inches(5.0), Inches(0.5),
                "研究の背景と動機", font_size=20, bold=True, color=COLOR_ACCENT)
    add_textbox(slide, Inches(1.1), Inches(2.6), Inches(5.0), Inches(1.5),
                "若者におけるソーシャルメディア利用の急増と、メンタルヘルス問題の増加の関連性についての関心が高まっている。",
                font_size=16, color=COLOR_TEXT)

    add_textbox(slide, Inches(1.1), Inches(4.0), Inches(5.0), Inches(0.5),
                "研究の目的と重要性", font_size=20, bold=True, color=COLOR_ACCENT)
    add_textbox(slide, Inches(1.1), Inches(4.6), Inches(5.0), Inches(1.5),
                "関連性を計量的に検証し、政策的な示唆を提供することを目的とする。",
                font_size=16, color=COLOR_TEXT)

    # Right column
    add_shape(slide, Inches(6.8), Inches(1.8), Inches(5.5), Inches(4.8), COLOR_LIGHT_BG)
    add_textbox(slide, Inches(7.1), Inches(2.0), Inches(5.0), Inches(0.5),
                "文献レビューと研究の位置づけ", font_size=20, bold=True, color=COLOR_ACCENT)
    add_textbox(slide, Inches(7.1), Inches(2.6), Inches(5.0), Inches(1.5),
                "これまでの研究で明らかにされていることと、本研究が新たに提供する知見について述べる。",
                font_size=16, color=COLOR_TEXT)

    add_textbox(slide, Inches(7.1), Inches(4.0), Inches(5.0), Inches(0.5),
                "論文の構成", font_size=20, bold=True, color=COLOR_ACCENT)
    add_textbox(slide, Inches(7.1), Inches(4.6), Inches(5.0), Inches(1.5),
                "データ → 実証モデル → 結果 → 結論の順に構成。",
                font_size=16, color=COLOR_TEXT)


def create_data_slide():
    """Slide 4: Data."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, COLOR_WHITE)
    add_section_header(slide)

    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(10), Inches(0.8),
                "2. データ", font_size=32, bold=True, color=COLOR_PRIMARY)

    items = [
        ("使用データの概要",
         "若者を対象とした大規模なアンケート調査データ、\nまたは公開されているデータベースを用いる。"),
        ("変数の定義と記述統計",
         "ソーシャルメディア利用時間（説明変数）、\nメンタルヘルス指標：うつ症状・不安感など（被説明変数）。"),
        ("データの前処理",
         "欠測データの処理や異常値の取り扱い方法について説明する。"),
        ("データの限界と制約",
         "データに関する制約やバイアスの可能性を考慮する。"),
    ]

    for i, (title, desc) in enumerate(items):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.8 + row * 2.5)

        add_shape(slide, x, y, Inches(5.5), Inches(2.2), COLOR_LIGHT_BG)
        add_textbox(slide, x + Inches(0.3), y + Inches(0.2), Inches(4.9), Inches(0.5),
                    title, font_size=18, bold=True, color=COLOR_ACCENT)
        add_textbox(slide, x + Inches(0.3), y + Inches(0.8), Inches(4.9), Inches(1.2),
                    desc, font_size=14, color=COLOR_TEXT)


def create_method_slide():
    """Slide 5: Methods."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, COLOR_WHITE)
    add_section_header(slide)

    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(10), Inches(0.8),
                "3. 実証モデルと分析手法", font_size=32, bold=True, color=COLOR_PRIMARY)

    items = [
        ("理論的背景と仮説",
         "ソーシャルメディア利用がメンタルヘルスに\n負の影響を与えるという仮説を設定。"),
        ("実証モデルの概要",
         "ソーシャルメディア利用時間を説明変数、\nメンタルヘルス指標をアウトカム変数とした\n回帰モデルを推定する。"),
        ("分析手法の詳細",
         "因果関係の検証に適した\nミクロ計量的手法を用いる。"),
    ]

    for i, (title, desc) in enumerate(items):
        x = Inches(0.8 + i * 4.0)
        add_shape(slide, x, Inches(1.8), Inches(3.7), Inches(4.5), COLOR_LIGHT_BG)
        # Number circle
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(1.45), Inches(2.1), Inches(0.8), Inches(0.8))
        circle.fill.solid()
        circle.fill.fore_color.rgb = COLOR_ACCENT
        circle.line.fill.background()
        tf = circle.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = str(i + 1)
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.font.name = "Meiryo"
        p.alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].space_before = Pt(0)

        add_textbox(slide, x + Inches(0.3), Inches(3.2), Inches(3.1), Inches(0.5),
                    title, font_size=18, bold=True, color=COLOR_ACCENT, alignment=PP_ALIGN.CENTER)
        add_textbox(slide, x + Inches(0.3), Inches(3.9), Inches(3.1), Inches(2.0),
                    desc, font_size=14, color=COLOR_TEXT, alignment=PP_ALIGN.CENTER)


def create_results_slide():
    """Slide 6: Results."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, COLOR_WHITE)
    add_section_header(slide)

    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(10), Inches(0.8),
                "4. 結果", font_size=32, bold=True, color=COLOR_PRIMARY)

    items = [
        ("主要な結果",
         "ソーシャルメディア利用がメンタルヘルスに与える影響についての主要な結果を示す。"),
        ("ロバスト性の検証",
         "結果が様々な条件下でも一貫しているかを検証する。"),
        ("サブサンプル・感度分析",
         "年齢層や性別、ソーシャルメディアの種類別などのサブグループ分析を行う。"),
        ("社会的・政策的含意",
         "若者のメンタルヘルスに対するソーシャルメディアの影響について、政策的な示唆を提供する。"),
    ]

    for i, (title, desc) in enumerate(items):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.8 + row * 2.5)

        add_shape(slide, x, y, Inches(5.5), Inches(2.2), COLOR_LIGHT_BG)
        # Accent left bar
        add_shape(slide, x, y, Inches(0.08), Inches(2.2), COLOR_ACCENT)
        add_textbox(slide, x + Inches(0.4), y + Inches(0.2), Inches(4.8), Inches(0.5),
                    title, font_size=18, bold=True, color=COLOR_ACCENT)
        add_textbox(slide, x + Inches(0.4), y + Inches(0.8), Inches(4.8), Inches(1.2),
                    desc, font_size=14, color=COLOR_TEXT)


def create_conclusion_slide():
    """Slide 7: Conclusion."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, COLOR_WHITE)
    add_section_header(slide)

    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(10), Inches(0.8),
                "5. 結論", font_size=32, bold=True, color=COLOR_PRIMARY)

    items = [
        ("研究の要約", "主要な結果とその意味を簡潔にまとめる。"),
        ("研究の貢献", "既存の知識にどのように貢献するかを述べる。"),
        ("研究の限界と今後の課題", "制約や今後取り組むべき課題について議論する。"),
        ("政策提言", "ソーシャルメディア利用に対する政策的な提言を行う。"),
    ]

    for i, (title, desc) in enumerate(items):
        x = Inches(0.8)
        y = Inches(1.8 + i * 1.3)

        add_shape(slide, x, y, Inches(11.5), Inches(1.1), COLOR_LIGHT_BG)
        add_shape(slide, x, y, Inches(0.08), Inches(1.1), COLOR_ACCENT)
        add_textbox(slide, x + Inches(0.4), y + Inches(0.1), Inches(3.5), Inches(0.5),
                    title, font_size=18, bold=True, color=COLOR_ACCENT)
        add_textbox(slide, x + Inches(4.2), y + Inches(0.1), Inches(7.0), Inches(0.9),
                    desc, font_size=16, color=COLOR_TEXT)


def create_references_slide():
    """Slide 8: References."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, COLOR_WHITE)
    add_section_header(slide)

    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(10), Inches(0.8),
                "参考文献", font_size=32, bold=True, color=COLOR_PRIMARY)

    add_textbox(slide, Inches(1.2), Inches(1.8), Inches(10), Inches(1.0),
                "参考にした文献の一覧（著者名、出版年、タイトル、出版社、ページ番号）",
                font_size=18, color=COLOR_TEXT)

    add_textbox(slide, Inches(1.2), Inches(3.5), Inches(10), Inches(1.0),
                "付録（必要に応じて）", font_size=24, bold=True, color=COLOR_PRIMARY)
    items = [
        "追加の分析結果や図表",
        "分析に使用したプログラムコードや計算手順",
    ]
    add_bullet_slide(slide, items, Inches(1.5), Inches(4.3), Inches(10), Inches(2.0),
                     font_size=18, color=COLOR_TEXT)


def create_closing_slide():
    """Slide 9: Thank you slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, COLOR_PRIMARY)

    add_shape(slide, Inches(4.0), Inches(2.8), Inches(1.0), Inches(0.06), COLOR_ACCENT)

    add_textbox(slide, Inches(1.5), Inches(3.0), Inches(10), Inches(1.2),
                "ご清聴ありがとうございました",
                font_size=40, bold=True, color=COLOR_WHITE, alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(1.5), Inches(4.5), Inches(10), Inches(0.8),
                "ご質問・ご意見をお待ちしております",
                font_size=20, color=RGBColor(0xAE, 0xBF, 0xD5), alignment=PP_ALIGN.CENTER)


# --- Build all slides ---
create_title_slide()
create_agenda_slide()
create_intro_slide()
create_data_slide()
create_method_slide()
create_results_slide()
create_conclusion_slide()
create_references_slide()
create_closing_slide()

output_path = "/home/user/test/presentation.pptx"
prs.save(output_path)
print(f"Presentation saved to {output_path}")
