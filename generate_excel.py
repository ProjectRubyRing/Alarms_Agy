# -*- coding: utf-8 -*-
"""
AWS CloudWatch Logs to JP1/IM Monitoring Architecture Design Generator
Creates a professionally styled Excel workbook with Meiryo UI font and Monotone palette.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_workbook(filename="AWS_CloudWatch_to_JP1_Monitoring_Design.xlsx"):
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # -------------------------------------------------------------
    # Styling Palette (Monotone Base / Meiryo UI)
    # -------------------------------------------------------------
    FONT_NAME = "Meiryo UI"

    font_title = Font(name=FONT_NAME, size=16, bold=True, color="FFFFFF")
    font_section = Font(name=FONT_NAME, size=12, bold=True, color="FFFFFF")
    font_sub_section = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
    font_header = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    font_data = Font(name=FONT_NAME, size=9.5, bold=False, color="1A1A1A")
    font_data_bold = Font(name=FONT_NAME, size=9.5, bold=True, color="1A1A1A")
    font_data_code = Font(name=FONT_NAME, size=9, bold=False, color="222222")
    font_note = Font(name=FONT_NAME, size=8.5, italic=True, color="555555")

    # Fills (Monotone Palette)
    fill_title = PatternFill(start_color="262626", end_color="262626", fill_type="solid")      # Almost Black
    fill_section = PatternFill(start_color="404040", end_color="404040", fill_type="solid")    # Dark Charcoal
    fill_sub_section = PatternFill(start_color="595959", end_color="595959", fill_type="solid")# Medium Dark Slate
    fill_header = PatternFill(start_color="4A4A4A", end_color="4A4A4A", fill_type="solid")     # Medium Charcoal
    fill_zebra_even = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid") # Pure White
    fill_zebra_odd = PatternFill(start_color="F7F7F8", end_color="F7F7F8", fill_type="solid")  # Extremely Soft Gray
    fill_highlight = PatternFill(start_color="EBEBEB", end_color="EBEBEB", fill_type="solid")  # Subtle Gray Accent
    fill_accent_header = PatternFill(start_color="333333", end_color="333333", fill_type="solid")

    # Borders
    border_thin_gray = Side(border_style="thin", color="CCCCCC")
    border_medium_gray = Side(border_style="medium", color="666666")
    border_double_bottom = Side(border_style="double", color="333333")

    cell_border = Border(left=border_thin_gray, right=border_thin_gray, top=border_thin_gray, bottom=border_thin_gray)
    header_border = Border(left=border_thin_gray, right=border_thin_gray, top=border_medium_gray, bottom=border_medium_gray)
    section_border = Border(left=border_medium_gray, right=border_medium_gray, top=border_medium_gray, bottom=border_medium_gray)

    # Alignments
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center", wrap_text=True)
    align_top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)

    def apply_row_style(ws, row_idx, font=font_data, fill=fill_zebra_even, border=cell_border, alignment=align_top_left):
        for cell in ws[row_idx]:
            if font: cell.font = font
            if fill: cell.fill = fill
            if border: cell.border = border
            if alignment: cell.alignment = alignment

    def set_column_widths_and_views(ws, col_widths, freeze="A5"):
        ws.views.sheetView[0].showGridLines = True
        if freeze:
            ws.freeze_panes = freeze
        for col_idx, width in enumerate(col_widths, start=1):
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = width

    # =========================================================================
    # SHEET 1: 01_概要・歴史と背景・小学生解説
    # =========================================================================
    ws1 = wb.create_sheet(title="01_概要・歴史と小学生解説")
    
    # Title
    ws1.merge_cells("A1:G1")
    ws1["A1"] = "【基本設計書】AWS CloudWatch Logs → JP1/IM 統合アラート監視アーキテクチャ概要"
    ws1["A1"].font = font_title
    ws1["A1"].fill = fill_title
    ws1["A1"].alignment = align_center
    ws1.row_dimensions[1].height = 40

    # Sub-banner
    ws1.merge_cells("A2:G2")
    ws1["A2"] = "システム全体像・登場の歴史と背景・非同期バッファリング構成の必然性・小学生向け直感解説"
    ws1["A2"].font = Font(name=FONT_NAME, size=10, italic=True, color="E0E0E0")
    ws1["A2"].fill = fill_accent_header
    ws1["A2"].alignment = align_center
    ws1.row_dimensions[2].height = 24

    ws1.row_dimensions[3].height = 10 # Blank spacer

    # Section 1: Executive Summary
    row = 4
    ws1.merge_cells(f"A{row}:G{row}")
    ws1[f"A{row}"] = "1. システム監視構成の目的とエグゼクティブサマリー"
    ws1[f"A{row}"].font = font_section
    ws1[f"A{row}"].fill = fill_section
    ws1[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[row].height = 28

    headers_summary = ["項目", "設計方針・概要", "技術要素 / 実装仕様", "メリット / 採用理由", "耐障害性 / ガバナンス"]
    row += 1
    ws1.row_dimensions[row].height = 24
    for c_idx, h in enumerate(headers_summary, start=1):
        cell = ws1.cell(row=row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.border = header_border
        cell.alignment = align_center
    ws1.merge_cells(f"B{row}:C{row}")
    ws1.merge_cells(f"D{row}:E{row}")
    ws1.merge_cells(f"F{row}:G{row}")

    summary_data = [
        ("監視対象と検知", "アプリケーション/コンテナ/サーバレスが出力するログ文字列をリアルタイム検知", "CloudWatch Logs + メトリクスフィルタ (Metric Filter)", "コード改修不要、正規表現でエラー文字列を数値メトリクスへ変換", "ログ未出力期間もデフォルト値0でMissing Data誤検知を完全防止"),
        ("アラーム判定", "規定期間における閾値超過判定とイベント発火", "CloudWatch Alarms (M out of N 評価)", "単発ノイズの静止化と確実なアラーム発行 (Sum >= 閾値)", "TreatMissingData=notBreaching による誤報防止"),
        ("メッセージ伝達", "マルチアカウント間をまたぐ疎結合なPub/Sub配信", "Amazon SNS (クロスアカウントサブスクリプション)", "VPC間ルーティング・ピアリング不要でAWSバックボーン直接連携", "高可用マネージドサービスによる耐障害性・高スループット"),
        ("耐障害バッファ", "アラートストーム吸収とJP1保守時のデータロスト防止", "Amazon SQS (共通運用アカウント側スタンダードキュー)", "最大14日間の永続保持、ロングポーリングによるAPIコスト削減", "Dead Letter Queue (DLQ) による異常メッセージの安全隔離"),
        ("JP1連携ワーカー", "メッセージ解読、ログ情報補完、JP1イベント形式への変換", "EC2アラート通知サーバ (常駐Python/Goデーモン)", "JP1/Baseのjevesendコマンドによる確実なJP1イベント発行", "システム障害時の流量制御（バックプレッシャー）と安全なリトライ"),
        ("全社統合管理", "全社システム障害の一元可視化・重要度別自動オペレーション", "JP1/Integrated Management (JP1/IM-View / Manager)", "24時間365日の運用監視員による統合コンソール監視と自動アクション", "重大度に応じたパトランプ鳴動、メール・自動電話、ServiceNow連携")
    ]

    for item in summary_data:
        row += 1
        ws1.row_dimensions[row].height = 30
        c1 = ws1.cell(row=row, column=1, value=item[0])
        c2 = ws1.cell(row=row, column=2, value=item[1])
        c3 = ws1.cell(row=row, column=3, value=item[2])
        c4 = ws1.cell(row=row, column=4, value=item[3])
        c5 = ws1.cell(row=row, column=5, value=item[4])
        ws1.merge_cells(f"B{row}:C{row}")
        ws1.merge_cells(f"D{row}:E{row}")
        ws1.merge_cells(f"F{row}:G{row}")
        fill_cur = fill_zebra_even if row % 2 == 0 else fill_zebra_odd
        apply_row_style(ws1, row, fill=fill_cur)
        c1.alignment = align_center
        c1.font = font_data_bold

    row += 2
    ws1.row_dimensions[row].height = 28
    ws1.merge_cells(f"A{row}:G{row}")
    ws1[f"A{row}"] = "2. 登場の歴史と背景：なぜこのアーキテクチャが必要になったのか？"
    ws1[f"A{row}"].font = font_section
    ws1[f"A{row}"].fill = fill_section
    ws1[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    row += 1
    headers_hist = ["時代区分", "監視アーキテクチャの形態", "運用の実態・技術的背景", "直面した重大な課題・障害リスク", "本設計による根本的解決策"]
    ws1.row_dimensions[row].height = 24
    for c_idx, h in enumerate(headers_hist, start=1):
        cell = ws1.cell(row=row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.border = header_border
        cell.alignment = align_center
    ws1.merge_cells(f"B{row}:C{row}")
    ws1.merge_cells(f"D{row}:E{row}")
    ws1.merge_cells(f"F{row}:G{row}")

    hist_data = [
        ("第1世代: オンプレミス時代\n(2000年代〜2010年代前半)", 
         "JP1/Base エージェント集中監視", 
         "全物理サーバ/VMにJP1/Baseを常駐インストール。ローカルのログファイルを「ログトラップ機能」が直接読み、閉域網内でJP1マネージャーへ直接ソケット通信。", 
         "・静的IPと固定台数が前提\n・オートスケーリングやコンテナに対応不可\n・エージェントのライセンス費用・配布・保守の肥大化", 
         "・クラウドネイティブ化：ログはすべてCloudWatch Logsへ集約しエージェントレス化を実現"),
        
        ("第2世代: クラウド移行初期\n(2010年代中盤〜後半)", 
         "CloudWatchから直接通知\n(直接同期連携の罠)", 
         "CloudWatch AlarmからWebhook、またはLambda経由でオンプレミスJP1サーバへ直接HTTPS/ソケット通信でプッシュ通知。", 
         "【重大事故①：アラートストームでのJP1ダウン】システム障害時に1秒数万件のエラーログが出るとJP1がパンク・沈黙\n【重大事故②：JP1保守時のアラート完全消失】JP1停止中に飛んできたアラームが再試行されずロスト\n【重大事故③：ネットワークのスパゲッティ化】各AWSアカウントからオンプレへDirect Connectやピアリングを個別接続し境界防御が崩壊", 
         "・「非同期メッセージキュー（SQS）」によるバッファリング導入\n・大量発生したアラートをSQSが安全に溜め込み、JP1の許容量に合わせて一定速度で処理（流量制御）\n・JP1が停止していても最大14日間メッセージが消失しない仕組みを確立"),
        
        ("第3世代: 現代の標準構成\n(マルチアカウント統制時代)", 
         "SNS + クロスアカウントSQS +\nEC2ワーカーによる疎結合連携", 
         "マルチアカウント環境（AWS Organizations）において、アプリ側はSNSへのPublishのみ。共通運用アカウントのSQSで一括受領し、EC2デーモンがJP1へ注入。", 
         "・アカウント間のセキュリティ境界の維持\n・暗号化キー（KMS）やIAMリソースポリシーの厳格化\n・アプリ開発側とインフラ運用側の責務の分離", 
         "・AWSバックボーン完結のクロスアカウントSNS→SQS配信により、VPC間ルーティング・IP重複問題をゼロ化\n・アプリ側はJP1の仕様（イベントID等）を意識せず、CloudWatch Logsにログを吐くだけで完結")
    ]

    for item in hist_data:
        row += 1
        ws1.row_dimensions[row].height = 58
        c1 = ws1.cell(row=row, column=1, value=item[0])
        c2 = ws1.cell(row=row, column=2, value=item[1])
        c3 = ws1.cell(row=row, column=3, value=item[2])
        c4 = ws1.cell(row=row, column=4, value=item[3])
        c5 = ws1.cell(row=row, column=5, value=item[4])
        ws1.merge_cells(f"B{row}:C{row}")
        ws1.merge_cells(f"D{row}:E{row}")
        ws1.merge_cells(f"F{row}:G{row}")
        fill_cur = fill_zebra_even if row % 2 == 0 else fill_zebra_odd
        apply_row_style(ws1, row, fill=fill_cur)
        c1.alignment = align_center
        c1.font = font_data_bold

    row += 2
    ws1.row_dimensions[row].height = 28
    ws1.merge_cells(f"A{row}:G{row}")
    ws1[f"A{row}"] = "3. 小学生にもわかる！たとえ話で理解するシステム全体の仕組み"
    ws1[f"A{row}"].font = font_section
    ws1[f"A{row}"].fill = fill_section
    ws1[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    row += 1
    headers_kid = ["システム部品名", "身近な学校のたとえ", "学校での具体的なお仕事・役割", "実際のITシステムでの動き", "もしこの部品が無かったらどうなる？"]
    ws1.row_dimensions[row].height = 24
    for c_idx, h in enumerate(headers_kid, start=1):
        cell = ws1.cell(row=row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.border = header_border
        cell.alignment = align_center
    ws1.merge_cells(f"B{row}:C{row}")
    ws1.merge_cells(f"D{row}:E{row}")
    ws1.merge_cells(f"F{row}:G{row}")

    kid_data = [
        ("CloudWatch Logs", "毎日の「連絡帳・日記」", "生徒（プログラム）が『今日何があったか』をどんどん書き込むノート。", "サーバやアプリが動いた記録（ログ）がリアルタイムに全部集まる場所。", "何が起きたのか後から誰も調べられず、原因不明の迷宮入りになる。"),
        ("メトリクスフィルタ", "連絡帳の「赤ペン先生」", "連絡帳の中から『ケンカした』『ケガした』という危ない言葉だけを探して、正の字を書いて数を数える先生。", "ログの中に『ERROR』や『FATAL』という文字列がないか見張り、見つけたら数字の1をカウントする。", "普通のつぶやきと大事件の区別がつかず、どれだけ事件が起きているか分からない。"),
        ("CloudWatch Alarms", "校内の「パトロール隊長」", "赤ペン先生のカウンターを見て、『5分間に3回以上ケンカが起きたら非常ベルを押すぞ！』と見張る隊長。", "メトリクスの数字を見て、決めたルール（閾値: 1分間に1回以上など）を超えたら警報を鳴らす。", "事件が多発しても誰も気付かず、手遅れになるまで放置されてしまう。"),
        ("Amazon SNS", "職員室への「校内放送スピーカー」", "非常ベルが鳴ると、『ピンポンパンポン！1組で事件発生！』と大音量で離れた職員室にアナウンスを飛ばすスピーカー。", "アラームが鳴った瞬間に、決められた宛先（運用チームのポスト）へ電波を飛ばして伝える。", "警報が鳴っても自分の教室の中だけで響いて、職員室の先生に届かない。"),
        ("Amazon SQS\n(共通運用アカウント)", "職員室の「頑丈な郵便ポスト」\n★一番大事なクッション！", "放送を聞いた連絡員が投函する手紙受け。ポストには何千通も手紙が入り、雨が降っても14日間絶対に手紙が消えない。", "アラートを一時的に安全に溜めておく『キュー』。後着のサーバが忙しくてもメッセージを1個も落とさず保持する。", "★大パニック！100人が一斉に校長室に走り込んで校長先生が気絶する（サーバがパンクして落ちる）。"),
        ("アラート通知サーバ\n(EC2)", "郵便ポストを見張る「当直の先生」", "ポストから手紙を1通ずつ丁寧に取り出して、校長先生が読みやすい『特大報告カード』に清書して書き直す配達係の先生。", "SQSからアラートをロングポーリングで取得し、JP1が理解できる形式（JP1イベント）にデータを変換する。", "手紙の内容が難しすぎて校長先生の電子黒板に映せず、誰も読めない。"),
        ("JP1/IM サーバ", "校長室の「巨大な電子掲示板」", "全校生徒のトラブルが一目でピカピカ光ってわかる司令塔の画面。校長先生が『すぐに現場へ急行！』と指示を出す。", "全社のエラーが一覧表示され、監視員が赤色・黄色のランプを見て即座に対応を開始する統合画面。", "会社中のどのシステムで何が壊れているのかバラバラで、誰も全体を把握できない。")
    ]

    for item in kid_data:
        row += 1
        ws1.row_dimensions[row].height = 42
        c1 = ws1.cell(row=row, column=1, value=item[0])
        c2 = ws1.cell(row=row, column=2, value=item[1])
        c3 = ws1.cell(row=row, column=3, value=item[2])
        c4 = ws1.cell(row=row, column=4, value=item[3])
        c5 = ws1.cell(row=row, column=5, value=item[4])
        ws1.merge_cells(f"B{row}:C{row}")
        ws1.merge_cells(f"D{row}:E{row}")
        ws1.merge_cells(f"F{row}:G{row}")
        fill_cur = fill_zebra_even if row % 2 == 0 else fill_zebra_odd
        apply_row_style(ws1, row, fill=fill_cur)
        c1.alignment = align_center
        c1.font = font_data_bold

    set_column_widths_and_views(ws1, [24, 28, 30, 36, 32, 28, 28])


    # =========================================================================
    # SHEET 2: 02_全体アーキテクチャ・動作原理
    # =========================================================================
    ws2 = wb.create_sheet(title="02_全体アーキテクチャ・動作原理")

    # Title
    ws2.merge_cells("A1:G1")
    ws2["A1"] = "【アーキテクチャ設計】全体構成図・データフロー・動作原理・シーケンス"
    ws2["A1"].font = font_title
    ws2["A1"].fill = fill_title
    ws2["A1"].alignment = align_center
    ws2.row_dimensions[1].height = 40

    ws2.merge_cells("A2:G2")
    ws2["A2"] = "アプリケーションアカウントと共通運用アカウントの責任分界点および非同期メッセージ伝達の詳細"
    ws2["A2"].font = Font(name=FONT_NAME, size=10, italic=True, color="E0E0E0")
    ws2["A2"].fill = fill_accent_header
    ws2["A2"].alignment = align_center
    ws2.row_dimensions[2].height = 24

    ws2.row_dimensions[3].height = 10

    # Section 1: Architecture Block Diagram
    row = 4
    ws2.merge_cells(f"A{row}:G{row}")
    ws2[f"A{row}"] = "1. エンドツーエンド・コンポーネント構成図（論理ブロック＆境界線）"
    ws2[f"A{row}"].font = font_section
    ws2[f"A{row}"].fill = fill_section
    ws2[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws2.row_dimensions[row].height = 28

    headers_arch = ["ステップ / 区分", "配置アカウント", "コンポーネント", "処理内容 / 動作原理", "入力データ", "出力データ / プロトコル", "耐障害・可用性の仕組み"]
    row += 1
    ws2.row_dimensions[row].height = 24
    for c_idx, h in enumerate(headers_arch, start=1):
        cell = ws2.cell(row=row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.border = header_border
        cell.alignment = align_center

    arch_data = [
        ("Step 1: ログ出力", "アプリ / システムアカウント\n(例: 111122223333)", "Application / ECS / Lambda", "アプリケーション処理中に例外や異常を検知し、標準出力またはログファイルへエラー文字列を出力", "業務トランザクションエラー", "ログレコード\n(JSON / テキスト形式)", "ローカルバッファリング、CloudWatch Agentによる再送"),
        ("Step 2: ログ集約", "アプリ / システムアカウント", "CloudWatch Logs\n(ロググループ)", "ストリームごとにログを受信し、インデックス化して暗号化ストレージに永続保存", "標準出力 / ログイベント", "ログイベントストリーム\n(保持期間管理)", "リージョン内マルチAZ自動複製、KMS暗号化"),
        ("Step 3: 文字列検知", "アプリ / システムアカウント", "メトリクスフィルタ\n(Metric Filter)", "ログ取り込みパイプライン内でパターンマッチングを実行し、マッチ時にメトリクスデータポイントを生成", "生ログストリーム", "CloudWatch Metric\n(Count = 1, Default = 0)", "マネージドインライン処理、ログ取り込みと同時に遅延なく評価"),
        ("Step 4: 閾値監視", "アプリ / システムアカウント", "CloudWatch Alarms\n(メトリクスアラーム)", "設定した評価期間（例: 1分間）ごとのメトリクス集計値を評価し、閾値超過時にALARM状態へ遷移", "メトリクス時系列データ\n(Statistic: Sum)", "ALARMステート変更イベント\n(CloudWatch Alarm JSON)", "評価期間 M out of N による一時スパイク誤報抑止"),
        ("Step 5: パブリッシュ", "アプリ / システムアカウント", "Amazon SNS\n(Standard Topic)", "CloudWatch Alarmのアクションとして起動され、トピックにバインドされたサブスクライバーへファンアウト配信", "Alarm JSONペイロード", "SNSメッセージ通知\n(HTTPS / AWS内部プロトコル)", "トピックへの複数回配信試行、AWS内部バックボーン通信"),
        ("Step 6: クロスアカウント受領", "共通運用アカウント\n(例: 999988887777)", "Amazon SQS\n(Standard Queue)", "SNSからの通知をクロスアカウントリソースポリシーに基づき受領し、FIFOではなく高スループットキューに格納", "SNSメッセージ", "永続化キューメッセージ\n(SQS Message ID / Body)", "最大14日間保持、DLQ（デッドレターキュー）による死活保護"),
        ("Step 7: メッセージ取得・変換", "共通運用アカウント", "EC2 アラート通知サーバ\n(Python/Go 常駐ワーカー)", "ロングポーリングでSQSからメッセージを取得、JSONをパースし、JP1イベント形式の属性（重大度・ID等）へマッピング", "SQSキューメッセージ\n(ReceiptHandle)", "JP1イベントパラメータ\n(jevesend 引数)", "可視性タイムアウトによる二重処理防止、処理成功後のみキュー削除"),
        ("Step 8: 統合監視連携", "オンプレミス / 共通運用VPC", "JP1/IM - Manager\n(JP1/Base イベントサービス)", "EC2から発行されたJP1イベントを受信し、統合イベントDBへ登録。JP1/IMコンソールへ赤/黄の重大度別表示と自動アクション実行", "JP1イベント\n(ポート 7365/tcp)", "JP1コンソール画面表示 / メール / 電話発呼", "イベントサービスの永続バッファ、JP1クラスタ構成対応")
    ]

    for item in arch_data:
        row += 1
        ws2.row_dimensions[row].height = 42
        for c_idx, val in enumerate(item, start=1):
            cell = ws2.cell(row=row, column=c_idx, value=val)
            if c_idx in (1, 2, 3):
                cell.alignment = align_center
                cell.font = font_data_bold if c_idx == 3 else font_data
            else:
                cell.alignment = align_top_left
                cell.font = font_data
            fill_cur = fill_zebra_even if row % 2 == 0 else fill_zebra_odd
            cell.fill = fill_cur
            cell.border = cell_border

    # Section 2: Detailed Sequence and Timing Flow
    row += 2
    ws2.merge_cells(f"A{row}:G{row}")
    ws2[f"A{row}"] = "2. 障害発生からJP1画面表示までのリアルタイム時系列シーケンス（レイテンシと各挙動）"
    ws2[f"A{row}"].font = font_section
    ws2[f"A{row}"].fill = fill_section
    ws2[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws2.row_dimensions[row].height = 28

    headers_seq = ["経過時間 (目安)", "実行主体 (Actor)", "処理フェーズ", "具体的な内部処理", "プロトコル / API", "データ状態の変化", "異常時のフォールバック"]
    row += 1
    ws2.row_dimensions[row].height = 24
    for c_idx, h in enumerate(headers_seq, start=1):
        cell = ws2.cell(row=row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.border = header_border
        cell.alignment = align_center

    seq_data = [
        ("T + 0.0 秒", "Application", "エラー発生・ログ出力", "アプリでDB接続失敗等の重大例外発生。logger.error('DB_CONNECTION_TIMEOUT') を出力", "ローカルI/O / stdout", "テキストログ生成", "アプリ側例外ハンドラで安全に切断"),
        ("T + 0.5〜1.0 秒", "CloudWatch Agent", "ログ転送", "コンテナ/EC2上のエージェントがログをバッファリングし、PutLogEvents APIで送信", "HTTPS (443)\nPutLogEvents", "CloudWatch Logsに取り込み", "ネットワーク瞬断時はローカルディスクにスプール"),
        ("T + 1.0〜1.5 秒", "Metric Filter", "パターンマッチング", "ログ取り込みエンジンが 'DB_CONNECTION_TIMEOUT' にマッチ。メトリクス AppErrorCount に 1 を計上", "CloudWatch 内部エンジン", "カスタムメトリクス生成", "パターン不一致時は無視（デフォルト値0維持）"),
        ("T + 60.0 秒\n(評価周期末)", "CloudWatch Alarms", "閾値評価・アラーム発火", "評価周期（1分）終了。Sum=1 >= 閾値(1) を検知。状態をOKからALARMへ変更しアクション実行", "CloudWatch Alarm Engine", "State: ALARM\nアラームJSON構築", "データ未達時はTreatMissingDataに従い評価"),
        ("T + 60.2 秒", "Amazon SNS", "クロスアカウント配信", "アラームアクションによりSNSトピックへメッセージを発行。運用アカウントのSQSへHTTPS Push", "HTTPS (AWSバックボーン)\nPublish / SendMessage", "SNS Message Envelope 付与", "配信失敗時は指数バックオフで再試行"),
        ("T + 60.5 秒", "Amazon SQS", "メッセージエンキュー", "運用アカウントSQSがメッセージを受信。アクセスポリシー・KMSキー検証を経てキューへ格納", "SQSマネージドストレージ", "Queue Message 可視状態", "最大保持期間（14日間）タイマースタート"),
        ("T + 60.6 秒", "EC2 通知サーバ", "ロングポーリング受信", "常駐スクリプトが ReceiveMessage (WaitTime=20s) で即座にメッセージを受領", "HTTPS (443)\nReceiveMessage", "メッセージ取得\n可視性タイムアウト開始(60s)", "サーバ停止時はSQS内に安全に滞留"),
        ("T + 60.8 秒", "EC2 通知サーバ", "データパース・変換", "SNS/Alarm JSONを解析。アラーム名、発生時刻、原因文字列を抽出し、JP1イベント引数を生成", "CPU内部処理 (Python/Go)", "jevesend 引数文字列構築", "パース失敗時はログ出力しDLQへ転送"),
        ("T + 61.2 秒", "EC2 / JP1 Client", "JP1イベント発行", "JP1/Base の jevesend コマンドをシェル実行。運用ネットワーク経由でJP1/IMサーバへ送信", "TCP (7365)\nJP1イベント通信", "JP1イベントパケット送信", "JP1停止時はリトライ。成功するまでSQS削除しない"),
        ("T + 61.5 秒", "JP1/IM Manager", "イベント受信・画面表示", "JP1/Baseイベントサービスがパケットを受領しDB登録。JP1/IMコンソールへ赤色の重大アラートを表示", "JP1内部イベントDB", "監視員コンソールに赤色点滅表示", "自動アクション定義に従いメール・電話発信")
    ]

    for item in seq_data:
        row += 1
        ws2.row_dimensions[row].height = 40
        for c_idx, val in enumerate(item, start=1):
            cell = ws2.cell(row=row, column=c_idx, value=val)
            if c_idx in (1, 2, 3):
                cell.alignment = align_center
                cell.font = font_data_bold if c_idx == 3 else font_data
            else:
                cell.alignment = align_top_left
                cell.font = font_data
            fill_cur = fill_zebra_even if row % 2 == 0 else fill_zebra_odd
            cell.fill = fill_cur
            cell.border = cell_border

    set_column_widths_and_views(ws2, [18, 20, 22, 38, 24, 28, 30])


    # =========================================================================
    # SHEET 3: 03_コンポーネント詳細設定値一覧
    # =========================================================================
    ws3 = wb.create_sheet(title="03_コンポーネント詳細設定値一覧")

    # Title
    ws3.merge_cells("A1:G1")
    ws3["A1"] = "【設定パラメータ仕様書】各コンポーネントで指定できる内容および推奨設定値一覧"
    ws3["A1"].font = font_title
    ws3["A1"].fill = fill_title
    ws3["A1"].alignment = align_center
    ws3.row_dimensions[1].height = 40

    ws3.merge_cells("A2:G2")
    ws3["A2"] = "CloudWatch Logs / Metric Filter / Alarms / SNS / SQS / EC2 Daemon / JP1各レイヤの完全定義"
    ws3["A2"].font = Font(name=FONT_NAME, size=10, italic=True, color="E0E0E0")
    ws3["A2"].fill = fill_accent_header
    ws3["A2"].alignment = align_center
    ws3.row_dimensions[2].height = 24

    ws3.row_dimensions[3].height = 10

    headers_params = ["コンポーネント", "設定パラメータ名", "設定内容・役割", "指定可能な値・選択肢", "現場での推奨設定値 (実例)", "設定理由・運用上の留意事項", "設定変更時の影響度"]
    
    components_params = [
        # 1. CloudWatch Logs
        ("CloudWatch Logs", "log_group_name", "ログを束ねるグループ名", "任意の文字列 (1〜512文字、英数字と記号)", "/aws/ecs/production-order-api", "システム・環境・サービス名が階層構造で判別できる命名規約に準拠", "高 (変更時は全フィルタ再作成)"),
        ("CloudWatch Logs", "retention_in_days", "ログデータの保持期限", "1, 3, 5, 7, 14, 30, 60, 90, 180, 365, 730, 無期限", "90 (日)", "監査要件とストレージ費用のバランス。長期保管ログはS3へエクスポート", "低 (ストレージコストのみ)"),
        ("CloudWatch Logs", "kms_key_id", "保存時暗号化に使用するKMSキー", "KMS Key ARN または未指定 (AWS所有キー)", "arn:aws:kms:ap-northeast-1:...:key/...", "金融・エンタープライズセキュリティ要件でCMK暗号化を適用", "中 (アクセス権限不備でログ書き込み拒否)"),

        # 2. Metric Filter
        ("メトリクスフィルタ", "filter_name", "フィルタの一意な識別名", "任意の文字列 (1〜512文字)", "MF-AppErrorCount-OrderApi", "メトリクスと対象ロググループが一目でわかる名称", "低"),
        ("メトリクスフィルタ", "filter_pattern", "抽出対象の文字列・正規表現パターン", "スペース区切り、JSON条件式、正規表現", "[timestamp, reqId, level = \"ERROR\" || level = \"FATAL\", ...]", "JSONログの場合は { $.level = \"ERROR\" } を推奨。テキストログは [..., level=\"ERROR\", ...]", "高 (パターンの誤りで未検知または誤検知発生)"),
        ("メトリクスフィルタ", "metric_name", "生成するカスタムメトリクス名", "任意の文字列 (英数字・記号)", "AppErrorCount", "CloudWatch Alarms側で参照するメトリクス名", "高 (アラーム側のメトリクス名と完全一致必須)"),
        ("メトリクスフィルタ", "metric_namespace", "メトリクスの所属名前空間", "任意の文字列 (AWS/プレフィックス以外)", "CustomApp/OrderService", "AWS標準名前空間と混同しないよう独自プレフィックスを使用", "高"),
        ("メトリクスフィルタ", "metric_value", "マッチ時に加算する数値", "数値 (通常は 1)", "1", "1件マッチするごとにカウントを1増やすため", "中"),
        ("メトリクスフィルタ", "default_value", "ログが出ない期間に代入する値\n★超重要パラメータ！", "0 または 空 (未指定)", "0", "【必須設定】未指定だとログが出ない時にデータ欠落(Missing Data)となりアラーム評価が不安定化する", "最高 (0を指定することで評価が極めて安定)"),
        ("メトリクスフィルタ", "unit", "メトリクスの単位", "Count, Seconds, Bytes, Percent 等", "Count", "回数をカウントするため", "低"),

        # 3. CloudWatch Alarms
        ("CloudWatch Alarms", "alarm_name", "アラームの表示名", "任意の文字列 (1〜255文字)", "ALARM-OrderApi-AppErrorCount-High", "アカウント名、システム名、監視項目、重大度を含める", "中 (通知メール・JP1画面のタイトルになる)"),
        ("CloudWatch Alarms", "comparison_operator", "閾値との比較条件", "GreaterThanOrEqualToThreshold,\nGreaterThanThreshold,\nLessThanThreshold 等", "GreaterThanOrEqualToThreshold\n(以上: >=)", "閾値1に対して、1回でもエラーが出たら発火させるため", "高"),
        ("CloudWatch Alarms", "evaluation_periods", "判定対象とするデータポイント数 (N)", "1 以上の整数", "1 (即時検知) または 3 (誤報抑止)", "即時通報が必要な重大エラーは1。断続的ノイズを除外したい場合は3", "高 (検知までの時間に直結)"),
        ("CloudWatch Alarms", "datapoints_to_alarm", "N個中何個閾値を超えたら発火するか (M)", "1 <= M <= N の整数", "1 (1 of 1) または 3 (3 of 3)", "M out of N 評価。1 of 1 で最速検知、3 of 3 でスパイク除外", "高"),
        ("CloudWatch Alarms", "period", "1データポイントの集計期間 (秒)", "10, 30, 60, 300, 900, 3600 (秒)", "60 (1分間)", "1分単位での集計。ログ監視では最速の検知が求められるため60秒推奨", "高"),
        ("CloudWatch Alarms", "statistic", "メトリクスの統計方法", "SampleCount, Average, Sum, Minimum, Maximum", "Sum (合計)", "1分間のエラー発生「総数」を評価するため", "高"),
        ("CloudWatch Alarms", "threshold", "発火の基準となる敷居値", "数値 (整数または小数)", "1.0", "1回でもERRORが出たらアラートを上げる場合は1。許容値がある場合は5など", "高"),
        ("CloudWatch Alarms", "treat_missing_data", "データが存在しない期間の扱い方", "missing, ignore, breaching, notBreaching", "notBreaching (正常とみなす)", "メトリクスフィルタでdefault_value=0を設定していれば実質0評価。安全弁としてnotBreaching推奨", "最高 (breachingにすると夜間ログがない時に誤報)"),
        ("CloudWatch Alarms", "alarm_actions", "ALARM状態遷移時の通知先アクション", "SNS Topic ARN、Lambda ARN、AutoScaling等", "arn:aws:sns:ap-northeast-1:111122223333:AppAlertTopic", "同一アカウント内のSNSトピックARNを指定", "最高 (指定漏れで通知が届かない)"),

        # 4. Amazon SNS
        ("Amazon SNS", "topic_name", "SNSトピックの名称", "任意の文字列 (英数字・ハイフン)", "App-Error-Alert-Topic", "用途（システム名・アラート用）が明確な名称", "中"),
        ("Amazon SNS", "fifo_topic", "FIFO(順序保証)かスタンダードか", "true (FIFO), false (スタンダード)", "false (スタンダードトピック)", "超高スループットが必要。アラーム通知では秒単位の順序厳密性より配信確実性を重視", "高"),
        ("Amazon SNS", "kms_master_key_id", "暗号化キーの指定", "alias/aws/sns または カスタマーCMK", "arn:aws:kms:... (CMK) または 未暗号化", "※重要：クロスアカウント配信時、alias/aws/sns(マネージドキー)はキーポリシー変更不可のため使えない。CMK必須", "最高 (暗号化設定不備でクロスアカウント送信失敗)"),
        ("Amazon SNS", "protocol", "サブスクリプションのプロトコル", "sqs, email, lambda, https 等", "sqs", "運用アカウントのSQSキューへ届けるため", "最高"),
        ("Amazon SNS", "endpoint", "サブスクリプションのエンドポイント", "宛先ARN (SQSキューARNなど)", "arn:aws:sqs:ap-northeast-1:999988887777:Shared-Ops-Alert-Queue", "共通運用アカウントのSQSキューARNを正確に指定", "最高"),
        ("Amazon SNS", "raw_message_delivery", "生メッセージ配信の有効無効", "true (生データのみ), false (SNSヘッダ付与)", "false (ヘッダー付きJSON)", "CloudWatch Alarmのメタ情報（MessageId, Timestamp, TopicArn）を保持したJSONを受信するため", "中"),

        # 5. Amazon SQS (共通運用アカウント)
        ("Amazon SQS", "queue_name", "SQSキューの名称", "任意の文字列 (英数字・ハイフン)", "Shared-Ops-Alert-Queue", "共通運用アカウントで監視アラート受信用であることが分かる名称", "中"),
        ("Amazon SQS", "fifo_queue", "FIFOキューかスタンダードキューか", "true, false", "false (スタンダードキュー)", "アラートストーム時（秒間数千件）でもスループット上限なしで受領するため", "高"),
        ("Amazon SQS", "message_retention_period", "メッセージ保持期間 (秒)", "60秒 〜 1,209,600秒 (14日間)", "1,209,600 (14日間: 最大値)", "JP1やEC2が障害・長期メンテで停止していても、絶対にメッセージを消失させないため最大値設定", "高"),
        ("Amazon SQS", "visibility_timeout", "可視性タイムアウト (秒)", "0秒 〜 43,200秒 (12時間)", "60 (秒)", "EC2ワーカーがメッセージを取得してからJP1送信・削除を完了するまでの時間。通常2〜3秒だが余裕を持たせる", "高 (短すぎると他プロセスが二重受信)"),
        ("Amazon SQS", "receive_wait_time_seconds", "メッセージ受信待機時間 (ロングポーリング)", "0秒 〜 20秒", "20 (秒: ロングポーリング最大値)", "【コスト・即時性の要】空振りのAPIリクエスト回数を劇的に減らし、メッセージ到着時は即座に受信", "高 (0にするとAPI費用が跳ね上がる)"),
        ("Amazon SQS", "max_receive_count", "DLQへ送るまでの最大受信回数", "1 以上の整数", "3 (回)", "3回連続で処理失敗（クラッシュ・フォーマットエラー等）したメッセージはDLQへ退避", "高 (設定しないと無限リトライループ)"),
        ("Amazon SQS", "dead_letter_queue_arn", "異常メッセージの退避先キューARN", "DLQのキューARN", "arn:aws:sqs:ap-northeast-1:999988887777:Shared-Ops-Alert-DLQ", "隔離されたメッセージを後から手動調査・再送するため", "高"),

        # 6. アラート通知サーバ (EC2)
        ("アラート通知サーバ (EC2)", "instance_type", "EC2インスタンスタイプ", "t4g.small / t3.micro 等", "t4g.small (Graviton3)", "CPU/メモリ負荷は極めて軽微。ネットワーク安定性とコスト効率を両立", "低"),
        ("アラート通知サーバ (EC2)", "polling_daemon_workers", "並行ポーリングワーカースレッド数", "1 〜 10 スレッド", "2 〜 4 ワーカー", "SQSから同時に受信・JP1へ投げるスレッド数。JP1サーバへの負荷集中を防ぐため少なめに設定", "中"),
        ("アラート通知サーバ (EC2)", "max_number_of_messages", "1回のポーリングで取得する最大件数", "1 〜 10 件", "10 (件)", "大量発生時の処理効率向上のため最大値10を指定", "中"),
        ("アラート通知サーバ (EC2)", "rate_limit_events_per_sec", "JP1への送信レートリミット (流量制御)", "任意の実数 (件/秒)", "20 (件/秒)", "JP1/Baseのイベント受信プロセスが過負荷でダウンするのを防止するためのバックプレッシャー制御", "高 (ストーム発生時のJP1保護)"),

        # 7. JP1/IM / JP1/Base
        ("JP1/IM / JP1/Base", "event_id", "JP1イベントの一意なID", "16進数 0:0〜7FFFFFFF:FFFFFFFF", "00000001 (ユーザー自由定義)", "運用チームで定めた「AWSアラート通知用イベントID」を付与", "高 (JP1コンソールでのフィルタ条件になる)"),
        ("JP1/IM / JP1/Base", "severity", "イベントの重大度 (Severity)", "Emergency, Alert, Critical, Error, Warning, Notice, Info, Debug", "Error (または Warning)", "CloudWatch Alarmのアラーム名や内容に応じて動的にマッピング。重大障害はError", "最高 (JP1画面の表示色・パトランプ・自動発報に直結)"),
        ("JP1/IM / JP1/Base", "message (-m)", "JP1コンソールに表示される主メッセージ", "文字列 (最大1,023バイト)", "[AWS-ALERT] [111122223333] ALARM-OrderApi-AppErrorCount-High (Count >= 1.0)", "運用監視員が一目でどのアカウントのどのシステムで何が起きたか把握できるフォーマット", "中"),
        ("JP1/IM / JP1/Base", "extended_attributes (-e)", "JP1イベント拡張属性", "KEY=VALUE 形式の複数属性", "E.AWS_ACCOUNT_ID=111122223333\nE.ALARM_NAME=ALARM-OrderApi-AppErrorCount-High\nE.METRIC=AppErrorCount", "JP1/IM側での自動アクション条件や詳細調査画面での参照用属性", "中")
    ]

    row = 4
    ws3.row_dimensions[row].height = 28
    for c_idx, h in enumerate(headers_params, start=1):
        cell = ws3.cell(row=row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.border = header_border
        cell.alignment = align_center

    cur_component = ""
    for item in components_params:
        row += 1
        ws3.row_dimensions[row].height = 36
        comp_name = item[0]
        
        for c_idx, val in enumerate(item, start=1):
            cell = ws3.cell(row=row, column=c_idx, value=val)
            if c_idx == 1:
                cell.alignment = align_center
                cell.font = font_data_bold
            elif c_idx in (2, 7):
                cell.alignment = align_center
                cell.font = font_data_bold if c_idx == 2 else font_data
            elif c_idx in (4, 5):
                cell.alignment = align_top_left
                cell.font = font_data_code if "arn:" in str(val) or "{" in str(val) or "0000" in str(val) else font_data
            else:
                cell.alignment = align_top_left
                cell.font = font_data

            fill_cur = fill_zebra_even if row % 2 == 0 else fill_zebra_odd
            cell.fill = fill_cur
            cell.border = cell_border

    set_column_widths_and_views(ws3, [22, 26, 32, 34, 38, 42, 24])


    # =========================================================================
    # SHEET 4: 04_クロスアカウント・セキュリティ設計
    # =========================================================================
    ws4 = wb.create_sheet(title="04_クロスアカウント・セキュリティ設計")

    # Title
    ws4.merge_cells("A1:G1")
    ws4["A1"] = "【セキュリティ＆権限設計】クロスアカウントSNS → SQS 連携ポリシー定義書"
    ws4["A1"].font = font_title
    ws4["A1"].fill = fill_title
    ws4["A1"].alignment = align_center
    ws4.row_dimensions[1].height = 40

    ws4.merge_cells("A2:G2")
    ws4["A2"] = "SQSリソースポリシー・KMS暗号化キーポリシー・EC2 IAMロール・不正書き込み防止のベストプラクティス"
    ws4["A2"].font = Font(name=FONT_NAME, size=10, italic=True, color="E0E0E0")
    ws4["A2"].fill = fill_accent_header
    ws4["A2"].alignment = align_center
    ws4.row_dimensions[2].height = 24

    ws4.row_dimensions[3].height = 10

    # Policy 1: SQS Queue Policy
    row = 4
    ws4.merge_cells(f"A{row}:G{row}")
    ws4[f"A{row}"] = "1. 共通運用アカウント側：SQSリソースポリシー (Queue Policy: 不正書き込み防止)"
    ws4[f"A{row}"].font = font_section
    ws4[f"A{row}"].fill = fill_section
    ws4[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[row].height = 28

    row += 1
    ws4.merge_cells(f"A{row}:G{row}")
    sqs_policy_desc = (
        "【重要セキュリティ要件】Principal に '*' を指定しつつ、Condition句で 'aws:SourceArn' を指定して送信元SNSトピックを完全制限します。\n"
        "これにより、認可されたアプリケーションアカウントのSNSトピックからのみ sqs:SendMessage を許可し、第三者によるキュー汚染を完全に遮断します。"
    )
    ws4[f"A{row}"] = sqs_policy_desc
    ws4[f"A{row}"].font = font_data
    ws4[f"A{row}"].fill = fill_highlight
    ws4[f"A{row}"].alignment = align_top_left
    ws4.row_dimensions[row].height = 42

    row += 1
    ws4.merge_cells(f"A{row}:G{row}")
    sqs_policy_json = """{
  "Version": "2012-10-17",
  "Id": "AllowCrossAccountSNSToPublishToSQS",
  "Statement": [
    {
      "Sid": "AllowAppAccountSNSMessages",
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:ap-northeast-1:999988887777:Shared-Ops-Alert-Queue",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:ap-northeast-1:111122223333:App-Error-Alert-Topic"
        }
      }
    }
  ]
}"""
    ws4[f"A{row}"] = sqs_policy_json
    ws4[f"A{row}"].font = font_data_code
    ws4[f"A{row}"].fill = fill_zebra_odd
    ws4[f"A{row}"].alignment = align_top_left
    ws4[f"A{row}"].border = cell_border
    ws4.row_dimensions[row].height = 250

    # Policy 2: KMS CMK Key Policy
    row += 1
    ws4.row_dimensions[row].height = 10

    row += 1
    ws4.merge_cells(f"A{row}:G{row}")
    ws4[f"A{row}"] = "2. 共通運用アカウント側：SQS暗号化用 KMS カスタマー管理キー (CMK) ポリシー"
    ws4[f"A{row}"].font = font_section
    ws4[f"A{row}"].fill = fill_section
    ws4[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[row].height = 28

    row += 1
    ws4.merge_cells(f"A{row}:G{row}")
    kms_policy_desc = (
        "【クロスアカウント暗号化の落とし穴】SQSをKMSで暗号化する場合、AWSマネージドキー (alias/aws/sqs) では外部アカウントのSNSからの書き込みが拒否されます。\n"
        "必ずカスタマー管理キー (CMK) を作成し、SNSサービスプリンシパルに対して 'kms:GenerateDataKey*' と 'kms:Decrypt' を明示的に許可する必要があります。"
    )
    ws4[f"A{row}"] = kms_policy_desc
    ws4[f"A{row}"].font = font_data
    ws4[f"A{row}"].fill = fill_highlight
    ws4[f"A{row}"].alignment = align_top_left
    ws4.row_dimensions[row].height = 42

    row += 1
    ws4.merge_cells(f"A{row}:G{row}")
    kms_policy_json = """{
  "Version": "2012-10-17",
  "Id": "AllowSNSToUseKMSKeyForSQSEncryption",
  "Statement": [
    {
      "Sid": "AllowRootAccountAdministration",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::999988887777:root"
      },
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "AllowSNSServiceToGenerateDataKeyAndDecrypt",
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": [
        "kms:GenerateDataKey*",
        "kms:Decrypt"
      ],
      "Resource": "*",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:ap-northeast-1:111122223333:App-Error-Alert-Topic"
        }
      }
    }
  ]
}"""
    ws4[f"A{row}"] = kms_policy_json
    ws4[f"A{row}"].font = font_data_code
    ws4[f"A{row}"].fill = fill_zebra_odd
    ws4[f"A{row}"].alignment = align_top_left
    ws4[f"A{row}"].border = cell_border
    ws4.row_dimensions[row].height = 360

    # Policy 3: EC2 Worker IAM Role Policy
    row += 1
    ws4.row_dimensions[row].height = 10

    row += 1
    ws4.merge_cells(f"A{row}:G{row}")
    ws4[f"A{row}"] = "3. EC2アラート通知サーバ用：最小権限 IAMポリシー (Instance Profile Policy)"
    ws4[f"A{row}"].font = font_section
    ws4[f"A{row}"].fill = fill_section
    ws4[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[row].height = 28

    row += 1
    ws4.merge_cells(f"A{row}:G{row}")
    ec2_policy_desc = (
        "EC2インスタンスにはSQSからのメッセージ受信、処理後の削除、キュー属性取得に必要な権限のみを最小特権で付与します。\n"
        "SQSがKMS暗号化されている場合は、対応する kms:Decrypt 権限も含めます。"
    )
    ws4[f"A{row}"] = ec2_policy_desc
    ws4[f"A{row}"].font = font_data
    ws4[f"A{row}"].fill = fill_highlight
    ws4[f"A{row}"].alignment = align_top_left
    ws4.row_dimensions[row].height = 36

    row += 1
    ws4.merge_cells(f"A{row}:G{row}")
    ec2_policy_json = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSQSMessageOperations",
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes",
        "sqs:GetQueueUrl"
      ],
      "Resource": [
        "arn:aws:sqs:ap-northeast-1:999988887777:Shared-Ops-Alert-Queue",
        "arn:aws:sqs:ap-northeast-1:999988887777:Shared-Ops-Alert-DLQ"
      ]
    },
    {
      "Sid": "AllowKMSDecryptForSQS",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:DescribeKey"
      ],
      "Resource": "arn:aws:kms:ap-northeast-1:999988887777:key/12345678-1234-1234-1234-123456789abc"
    }
  ]
}"""
    ws4[f"A{row}"] = ec2_policy_json
    ws4[f"A{row}"].font = font_data_code
    ws4[f"A{row}"].fill = fill_zebra_odd
    ws4[f"A{row}"].alignment = align_top_left
    ws4[f"A{row}"].border = cell_border
    ws4.row_dimensions[row].height = 350

    set_column_widths_and_views(ws4, [16, 20, 24, 28, 28, 28, 28])


    # =========================================================================
    # SHEET 5: 05_メッセージ変換・JP1連携例
    # =========================================================================
    ws5 = wb.create_sheet(title="05_メッセージ変換・JP1連携例")

    # Title
    ws5.merge_cells("A1:G1")
    ws5["A1"] = "【データ変換仕様書】CloudWatch Alarm JSON → JP1イベントへの完全マッピング"
    ws5["A1"].font = font_title
    ws5["A1"].fill = fill_title
    ws5["A1"].alignment = align_center
    ws5.row_dimensions[1].height = 40

    ws5.merge_cells("A2:G2")
    ws5["A2"] = "SQS受信メッセージ構造・EC2 Pythonパーサー実装・JP1 jevesend コマンド構文と属性定義"
    ws5["A2"].font = Font(name=FONT_NAME, size=10, italic=True, color="E0E0E0")
    ws5["A2"].fill = fill_accent_header
    ws5["A2"].alignment = align_center
    ws5.row_dimensions[2].height = 24

    ws5.row_dimensions[3].height = 10

    # Section 1: JSON Payloads
    row = 4
    ws5.merge_cells(f"A{row}:G{row}")
    ws5[f"A{row}"] = "1. SQSから受信する生メッセージ構造 (SNS Envelope 内部の CloudWatch Alarm JSON)"
    ws5[f"A{row}"].font = font_section
    ws5[f"A{row}"].fill = fill_section
    ws5[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[row].height = 28

    row += 1
    ws5.merge_cells(f"A{row}:G{row}")
    alarm_json_sample = """{
  "Type" : "Notification",
  "MessageId" : "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
  "TopicArn" : "arn:aws:sns:ap-northeast-1:111122223333:App-Error-Alert-Topic",
  "Subject" : "ALARM: \\"ALARM-OrderApi-AppErrorCount-High\\" in Asia Pacific (Tokyo)",
  "Message" : "{\\"AlarmName\\":\\"ALARM-OrderApi-AppErrorCount-High\\",\\"AlarmDescription\\":\\"注文APIエラーログ検知アラーム\\",\\"AWSAccountId\\":\\"111122223333\\",\\"NewStateValue\\":\\"ALARM\\",\\"NewStateReason\\":\\"Threshold Crossed: 1 datapoint [5.0 (07/10/26 04:00:00)] was greater than or equal to the threshold (1.0).\\",\\"StateChangeTime\\":\\"2026-10-07T04:01:15.123+0000\\",\\"Region\\":\\"Asia Pacific (Tokyo)\\",\\"AlarmArn\\":\\"arn:aws:cloudwatch:ap-northeast-1:111122223333:alarm:ALARM-OrderApi-AppErrorCount-High\\",\\"OldStateValue\\":\\"OK\\",\\"Trigger\\":{\\"MetricName\\":\\"AppErrorCount\\",\\"Namespace\\":\\"CustomApp/OrderService\\",\\"StatisticType\\":\\"Statistic\\",\\"Statistic\\":\\"SUM\\",\\"Unit\\":null,\\"Dimensions\\":[],\\"Period\\":60,\\"EvaluationPeriods\\":1,\\"ComparisonOperator\\":\\"GreaterThanOrEqualToThreshold\\",\\"Threshold\\":1.0}}",
  "Timestamp" : "2026-10-07T04:01:15.567Z"
}"""
    ws5[f"A{row}"] = alarm_json_sample
    ws5[f"A{row}"].font = font_data_code
    ws5[f"A{row}"].fill = fill_zebra_odd
    ws5[f"A{row}"].alignment = align_top_left
    ws5[f"A{row}"].border = cell_border
    ws5.row_dimensions[row].height = 200

    # Section 2: Mapping Table
    row += 1
    ws5.row_dimensions[row].height = 10

    row += 1
    ws5.merge_cells(f"A{row}:G{row}")
    ws5[f"A{row}"] = "2. CloudWatch Alarm JSON属性からJP1イベント属性へのマッピング定義表"
    ws5[f"A{row}"].font = font_section
    ws5[f"A{row}"].fill = fill_section
    ws5[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[row].height = 28

    headers_mapping = ["JP1イベント属性名", "JP1属性種別", "取得元 (CloudWatch JSONキー)", "変換ロジック・成型ルール", "設定例 (出力値)", "JP1コンソール上での用途"]
    row += 1
    ws5.row_dimensions[row].height = 24
    for c_idx, h in enumerate(headers_mapping, start=1):
        cell = ws5.cell(row=row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.border = header_border
        cell.alignment = align_center
    ws5.merge_cells(f"E{row}:F{row}")

    mapping_data = [
        ("イベントID (-i)", "基本属性", "固定値 (システム定義)", "AWSアラーム共通のイベントIDを16進数で指定", "00000001", "イベントフィルタリング・自動アクションのトリガー条件"),
        ("重大度 (-s / SEVERITY)", "拡張属性", "AlarmName または NewStateValue", "NewStateValue=='ALARM' かつ AlarmNameに'FATAL'や'Critical'を含む場合はEmergency/Critical、通常はError。'OK'復旧時はInfo", "Error", "JP1イベントコンソール上の表示色（赤: Error、黄: Warning、青: Info）"),
        ("メッセージ (-m / MESSAGE)", "基本属性", "AWSAccountId, AlarmName, NewStateReason", "成型文字列: '[AWS-ALERT] [{AWSAccountId}] {AlarmName} : {NewStateReason}'", "[AWS-ALERT] [111122223333] ALARM-OrderApi-AppErrorCount-High : Threshold Crossed...", "監視員が画面一覧で即座に状況を把握するメイン表示テキスト"),
        ("発生日時 (DATE / TIME)", "基本属性", "StateChangeTime", "ISO8601形式のタイムスタンプをローカルタイム (JST) へ変換してJP1/Baseへ引き渡し", "2026/10/07 13:01:15", "インシデント発生時刻の記録・ソート"),
        ("E.AWS_ACCOUNT_ID", "固有拡張属性", "AWSAccountId", "そのまま設定", "111122223333", "マルチアカウント環境における障害発生元AWSアカウントの特定・集計"),
        ("E.AWS_REGION", "固有拡張属性", "Region", "そのまま設定", "Asia Pacific (Tokyo)", "リージョン別インシデント分析"),
        ("E.ALARM_NAME", "固有拡張属性", "AlarmName", "そのまま設定", "ALARM-OrderApi-AppErrorCount-High", "アラーム名に基づく自動エスカレーション・マニュアルリンク表示"),
        ("E.METRIC_NAME", "固有拡張属性", "Trigger.MetricName", "そのまま設定", "AppErrorCount", "メトリクス種別の特定"),
        ("E.NAMESPACE", "固有拡張属性", "Trigger.Namespace", "そのまま設定", "CustomApp/OrderService", "システム・サービスの特定"),
        ("E.LOG_GROUP", "固有拡張属性", "AlarmDescription 等から抽出", "アラーム設定またはInsights連携によりロググループ名を補完", "/aws/ecs/production-order-api", "監視員が即座に対象ログをCloudWatchで開くためのディープリンク生成")
    ]

    for item in mapping_data:
        row += 1
        ws5.row_dimensions[row].height = 30
        c1 = ws5.cell(row=row, column=1, value=item[0])
        c2 = ws5.cell(row=row, column=2, value=item[1])
        c3 = ws5.cell(row=row, column=3, value=item[2])
        c4 = ws5.cell(row=row, column=4, value=item[3])
        c5 = ws5.cell(row=row, column=5, value=item[4])
        c6 = ws5.cell(row=row, column=6, value=item[5])
        ws5.merge_cells(f"E{row}:F{row}")
        fill_cur = fill_zebra_even if row % 2 == 0 else fill_zebra_odd
        apply_row_style(ws5, row, fill=fill_cur)
        c1.alignment = align_center
        c1.font = font_data_bold
        c2.alignment = align_center

    # Section 3: jevesend Command Example
    row += 2
    ws5.merge_cells(f"A{row}:G{row}")
    ws5[f"A{row}"] = "3. JP1イベント発行コマンド (jevesend) の実際の実行コマンドライン構文例"
    ws5[f"A{row}"].font = font_section
    ws5[f"A{row}"].fill = fill_section
    ws5[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[row].height = 28

    row += 1
    ws5.merge_cells(f"A{row}:G{row}")
    jevesend_cmd = """/opt/jp1base/bin/jevesend \\
  -d "JP1_DEFAULT" \\
  -i 00000001 \\
  -s Error \\
  -m "[AWS-ALERT] [111122223333] ALARM-OrderApi-AppErrorCount-High : Threshold Crossed (Count >= 1.0)" \\
  -e "SEVERITY=Error" \\
  -e "E.AWS_ACCOUNT_ID=111122223333" \\
  -e "E.ALARM_NAME=ALARM-OrderApi-AppErrorCount-High" \\
  -e "E.METRIC_NAME=AppErrorCount" \\
  -e "E.NAMESPACE=CustomApp/OrderService" \\
  -e "E.LOG_GROUP=/aws/ecs/production-order-api" \\
  -e "E.AWS_REGION=ap-northeast-1" """
    ws5[f"A{row}"] = jevesend_cmd
    ws5[f"A{row}"].font = font_data_code
    ws5[f"A{row}"].fill = fill_zebra_odd
    ws5[f"A{row}"].alignment = align_top_left
    ws5[f"A{row}"].border = cell_border
    ws5.row_dimensions[row].height = 180

    # Section 4: EC2 Worker Script Snippet
    row += 2
    ws5.merge_cells(f"A{row}:G{row}")
    ws5[f"A{row}"] = "4. EC2アラート通知デーモン 実装例 (Python 3 + boto3 + subprocess / jevesend)"
    ws5[f"A{row}"].font = font_section
    ws5[f"A{row}"].fill = fill_section
    ws5[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[row].height = 28

    row += 1
    ws5.merge_cells(f"A{row}:G{row}")
    ec2_script_snippet = """# -*- coding: utf-8 -*-
import json, subprocess, logging, time, boto3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sqs = boto3.client("sqs", region_name="ap-northeast-1")
QUEUE_URL = "https://sqs.ap-northeast-1.amazonaws.com/999988887777/Shared-Ops-Alert-Queue"

def forward_to_jp1(alarm_data):
    alarm_name = alarm_data.get("AlarmName", "UNKNOWN_ALARM")
    account_id = alarm_data.get("AWSAccountId", "UNKNOWN_ACCOUNT")
    reason = alarm_data.get("NewStateReason", "")
    trigger = alarm_data.get("Trigger", {})
    metric_name = trigger.get("MetricName", "")
    namespace = trigger.get("Namespace", "")
    
    # Severity判定
    state = alarm_data.get("NewStateValue", "ALARM")
    severity = "Error" if state == "ALARM" else "Notice"
    
    msg = f"[AWS-ALERT] [{account_id}] {alarm_name} : {reason}"[:1023]
    cmd = [
        "/opt/jp1base/bin/jevesend",
        "-d", "JP1_DEFAULT",
        "-i", "00000001",
        "-s", severity,
        "-m", msg,
        "-e", f"SEVERITY={severity}",
        "-e", f"E.AWS_ACCOUNT_ID={account_id}",
        "-e", f"E.ALARM_NAME={alarm_name}",
        "-e", f"E.METRIC_NAME={metric_name}",
        "-e", f"E.NAMESPACE={namespace}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    logging.info(f"JP1 event sent successfully: {alarm_name}")

def main():
    logging.info("Starting SQS to JP1 Alert Forwarder Daemon...")
    while True:
        try:
            resp = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20,  # Long Polling
                VisibilityTimeout=60
            )
            messages = resp.get("Messages", [])
            for msg in messages:
                body = json.loads(msg["Body"])
                # SNS Envelope内のMessageをパース
                alarm_data = json.loads(body["Message"]) if "Message" in body else body
                forward_to_jp1(alarm_data)
                sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])
                time.sleep(0.05)  # 流量制御 (最大20件/秒)
        except Exception as e:
            logging.error(f"Error processing alert: {e}", exc_info=True)
            time.sleep(5)

if __name__ == "__main__":
    main()"""
    ws5[f"A{row}"] = ec2_script_snippet
    ws5[f"A{row}"].font = font_data_code
    ws5[f"A{row}"].fill = fill_zebra_odd
    ws5[f"A{row}"].alignment = align_top_left
    ws5[f"A{row}"].border = cell_border
    ws5.row_dimensions[row].height = 420

    set_column_widths_and_views(ws5, [22, 16, 26, 36, 30, 30, 24])


    # =========================================================================
    # SHEET 6: 06_運用保守・障害設計
    # =========================================================================
    ws6 = wb.create_sheet(title="06_運用保守・障害設計")

    # Title
    ws6.merge_cells("A1:G1")
    ws6["A1"] = "【運用・非機能設計】耐障害性・アラートストーム対策・監視運用ベストプラクティス"
    ws6["A1"].font = font_title
    ws6["A1"].fill = fill_title
    ws6["A1"].alignment = align_center
    ws6.row_dimensions[1].height = 40

    ws6.merge_cells("A2:G2")
    ws6["A2"] = "大量アラーム時のフラッピング抑止、JP1計画停止時の運用、デッドレターキュー(DLQ)監視手順"
    ws6["A2"].font = Font(name=FONT_NAME, size=10, italic=True, color="E0E0E0")
    ws6["A2"].fill = fill_accent_header
    ws6["A2"].alignment = align_center
    ws6.row_dimensions[2].height = 24

    ws6.row_dimensions[3].height = 10

    headers_ops = ["設計領域", "想定される障害シナリオ / 課題", "アーキテクチャ上の防御メカニズム", "運用手順・リカバリアクション", "監視指標 (SLI/SLO) / 復旧目標 (RTO/RPO)"]
    row = 4
    ws6.row_dimensions[row].height = 24
    for c_idx, h in enumerate(headers_ops, start=1):
        cell = ws6.cell(row=row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.border = header_border
        cell.alignment = align_center
    ws6.merge_cells(f"B{row}:C{row}")
    ws6.merge_cells(f"D{row}:E{row}")
    ws6.merge_cells(f"F{row}:G{row}")

    ops_data = [
        ("アラートストーム\n(大量発生)", 
         "カスケード障害時、1秒間に数千〜数万件のエラーログが吹き出し、監視インフラ全体に過負荷がかかる。", 
         "1. メトリクスフィルタの集計（ログ件数を数値化し集約）\n2. SQSスタンダードキューによる無限バッファリング\n3. EC2通知ワーカーでの流量制御 (Rate Limiting: 例20件/秒)\n4. JP1/IMイベントコンソールでの重複抑止フィルタ機能", 
         "重大アラートはJP1に順次届けられ、破棄されない。監視員はJP1コンソールの集約ビューで根本原因ノードを特定。", 
         "・RPO = 0 (メッセージ消失ゼロ)\n・キュー滞留許容量: 120,000件以上"),
        
        ("JP1/IMサーバの\n計画停止・障害", 
         "JP1サーバのOSパッチ適用、メンテナンス、またはハードウェア障害によりJP1/Base受付ポートが応答しない。", 
         "1. EC2デーモンがjevesendのリターンコード異常を検知\n2. SQSメッセージを削除せず保持 (DeleteMessageをスキップ)\n3. 可視性タイムアウト経過後に自動的にキューへ再キューイング\n4. SQSの最大保持期間14日間により完全保護", 
         "JP1サーバ復旧後、EC2デーモンが自動的に未送信メッセージを再送開始。オペレータの手動リカバリ操作は一切不要。", 
         "・RTO = JP1サービス再開後 即時\n・最大許容停止時間: 14日間 (336時間)"),
        
        ("EC2通知サーバの\n単体障害", 
         "EC2インスタンスのハードウェア故障、OSハング、プロセス停止によりメッセージ処理が中断。", 
         "1. Auto Scaling Group (min=1, max=1) によるインスタンス自動再作成（セルフヒーリング）\n2. メッセージはSQSキューに安全に滞留\n3. 新インスタンス起動時にsystemdサービスが自動立ち上がり処理再開", 
         "CloudWatch AlarmでSQSの `ApproximateAgeOfOldestMessage` (最古メッセージ滞留時間) を監視し、15分超過でインフラ担当者へ通知。", 
         "・RTO = 3〜5分 (EC2自動再作成)\n・データ損失ゼロ (RPO=0)"),
        
        ("デッドレターキュー\n(DLQ) 滞留", 
         "予期せぬJSONフォーマット崩れや文字コード不正により、EC2デーモンが3回連続で処理失敗したメッセージが発生。", 
         "1. Redrive Policy (maxReceiveCount=3) により不正メッセージをメインキューからDLQへ隔離\n2. 正常なメッセージのパイプライン処理はブロックされずに継続（ヘッドオブラインブロッキング防止）", 
         "DLQの `ApproximateNumberOfMessagesVisible >= 1` を検知するCloudWatch Alarmを設定。運用者がDLQメッセージを手動解析しツールでRedrive。", 
         "・DLQ検知目標: 5分以内\n・原因究明とコード改修"),
        
        ("監視基盤自体の\n死活監視\n(監視の監視)", 
         "アラートパイプライン全体のどこかがサイレントに停止し、エラーが起きても気づかないリスク。", 
         "【Dead Man's Switch / 定期ハートビート】\n1. EventBridgeで毎日定期的にテストログをCloudWatch Logsへ投入\n2. JP1コンソールに「定期正常通信確認」イベントが届くことを確認\n3. 一定時間届かない場合にJP1側で欠落アラームを発動", 
         "監視網全体の健全性を日次で自動検証。設定ミスやポリシー変更によるサイレント障害を100%防止。", 
         "・ハートビート間隔: 24時間 (または1時間)\n・未達検知: 予定時刻+10分以内")
    ]

    for item in ops_data:
        row += 1
        ws6.row_dimensions[row].height = 64
        c1 = ws6.cell(row=row, column=1, value=item[0])
        c2 = ws6.cell(row=row, column=2, value=item[1])
        c3 = ws6.cell(row=row, column=3, value=item[2])
        c4 = ws6.cell(row=row, column=4, value=item[3])
        c5 = ws6.cell(row=row, column=5, value=item[4])
        ws6.merge_cells(f"B{row}:C{row}")
        ws6.merge_cells(f"D{row}:E{row}")
        ws6.merge_cells(f"F{row}:G{row}")
        fill_cur = fill_zebra_even if row % 2 == 0 else fill_zebra_odd
        apply_row_style(ws6, row, fill=fill_cur)
        c1.alignment = align_center
        c1.font = font_data_bold

    set_column_widths_and_views(ws6, [22, 28, 30, 36, 32, 28, 28])

    # Save workbook
    wb.save(filename)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_excel_workbook()
