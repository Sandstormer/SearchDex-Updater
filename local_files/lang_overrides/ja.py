headerNames = ['No.','画像','名前','タイプ','とくせい','タマゴ わざ','コスト',
               '合計','HP','攻撃','防御','特攻','特防','素早']
altText = ['わざ','規格のみ','隠れのみ','消極的のみ','検索の','威力','命中','PP',
           'フィルターに追加','きおくのキノコ','色違い','タマゴわざ','レアタマゴわざ',
           'コモン','スーパー','ハイパー','わざマシン','Lv.','進化','卵']
catToName = ['タイプ','とくせい','わざ','世代','コスト','タマゴ層','ゲームモード',
             'しんか','フォルム','バイオーム','関連','色違い','タグ']
infoText = ['アメごとのなつき度','パッシブ','ポイント削減','タマゴを買う','隠れ特性',
            'タマゴ 限定','ベイビィ限定','パラドックスポケモン','フォルムチェンジ','バイオーム','選択フィルタ',
            '## 個の卵後に減少','レベルで','タマゴで','わざマシンで']
biomeText = ['コモン','アンコモン','レア','スーパーレア','ウルトラレア','ボス','コモン','UC','レア','SR','UR','暁','昼','黄昏','夜']
phrases = {
    'exclusive': '限定',
    'new': '新しい',
    'tag': '属性',
    'theEnd': '終わり',
    'fullyEvolved': '最終進化',
    'formBase': '基本',
    'formMega': 'メガ',
    'formNewMega': '新メガ',
    'formGiga': 'キョダイ',
    'formTransformed': '変化',
    'lureAbility': 'おびき寄せ特性',
    'ignoresAbilities': '特性無視',
    'electricImmunity': 'でんき無効',
    'fireImmunity': 'ほのお無効',
    'waterImmunity': 'みず無効',
    'rainAbility': '雨 とくせい',
    'sandAbility': 'すなあらし とくせい',
    'snowAbility': 'ゆき とくせい',
    'sunAbility': '晴れ とくせい',
    'targetSwitchesOut': '強制交代',
    'spreadMoves': '範囲技',
}
substitutions = [ # Text shortenings to make it fit in the UI
    ["キョダイマックス","キョダイ"],
]
helpMenuText = [
'PokeRogue 用の <span style="color:rgb(140, 130, 240);">高速・強力な検索</span>',
'検索バーを使ってフィルターを追加：',
'複数のフィルターで絞り込めます',
'間をクリックして「OR」検索します',
'<span style="color:rgb(140, 130, 240);">ヘッダー</span> をクリックで並び替え',
'<b>${headerNames[1]}</b> 列では色違い（シャイニー）に限定可能です',
'<b>${headerNames[4]}</b> 列はスロット1つに絞れます：',
'メイン特性', '${infoText[4]}', '${infoText[1]}',
'<b>${headerNames[5]}</b> は <b>${fidToName[fidThreshold[4]]}</b> と <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[4]+1]}</span> として表示されます',
'ヘッダーをクリックして<b>${infoText[9]}</b>に切り替えます',
'この列には<b>${altText[0]}/${infoText[9]}</b>（フィルター済み）も表示されます',
'<b>${catToName[4]}</b> 列では <b>${catToName[5]}</b> の色を示します：',
'項目をクリックして詳細を表示します：',
'<b>${headerNames[2]}</b>をクリックして技構成を確認します。',
'<b>${altText[5]}</b>の色は<span style="color:${col.or}; font-weight: bold;">物理</span>または<span style="color:${col.bl}; font-weight: bold;">特殊</span>ダメージを示します',
'<b>${altText[6]}</b>の色は<span style="color:${col.re}; font-weight: bold;">複数対象</span>技を示します',
'このサイトは Sandstorm によって多大な努力のもと作成されました。クッキーは保存しておらず, 個人データの収集も行っていません。画像とゲームデータは PokeRogue の GitHub から取得しています。すべてのアセットの著作権は元の制作者に帰属します。',
'ゲームバージョン', '日付', 'フィルター保持',
]