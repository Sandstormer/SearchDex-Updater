headerNames = ['No.','画像','名前','タイプ','とくせい','タマゴ わざ','コスト','合計','HP','攻撃','防御','特攻','特防','素早']
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
helpMenuText = """
<b>PokeRogue 用の <span style="color:rgb(140, 130, 240);">高速・強力な検索</span></b>
<hr>
<p style="margin: 10px; font-weight: bold;">検索バーを使ってフィルターを追加：</p>
<p style="margin: 10px; font-weight: bold;"><span style="color:${typeColors[9]};">${catToName[0]}</span>, 
<span style="color:${fidToColor(fidThreshold[0])[0]};">${catToName[1]}</span>, 
<span style="color:${fidToColor(fidThreshold[1])[0]};">${catToName[2]}</span>, 
<span style="color:${fidToColor(fidThreshold[2])[0]};">${catToName[3]}</span>, 
<span style="color:${fidToColor(fidThreshold[3])[0]};">${catToName[4]}</span>, 
<span style="color:${fidToColor(fidThreshold[4])[0]};">${catToName[5]}</span>, <br>
<span style="color:${fidToColor(fidThreshold[5])[1]};">${catToName[6]}</span>, 
<span style="color:${eggTierColors(2)};">${catToName[7]}</span>, 
<span style="color:${fidToColor(fidThreshold[7])[0]};">${headerNames[1]}</span>, 
<span style="color:${fidToColor(fidThreshold[8])[0]};">${catToName[9]}</span></p>
フィルターを組み合わせて検索<br>
<span style="color:rgb(145, 145, 145);">クリックで「または」条件に変更</span>
<hr>
<p style="margin: 10px; font-weight: bold;"><span style="color:rgb(140, 130, 240);">ヘッダー</span> をクリックで並び替え</p>
<b>${headerNames[1]}</b> 列では色違い（シャイニー）に限定可能です  
<p style="margin: 10px;"><b>${headerNames[4]}</b> 列はスロット1つに絞れます: <br>
<b>メイン特性</b>,  
<span style="color:rgb(240, 230, 140); font-weight: bold;">${infoText[4]}</span>,  
<span style="color:rgb(140, 130, 240); font-weight: bold;">${infoText[1]}</span></p>
<b>${headerNames[5]}</b> は <b>${fidToName[fidThreshold[6]]}</b> と <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[6]+1]}</span> として表示されます<br> 
<span style="color:rgb(145, 145, 145);">フィルターされた技の入手元も表示可能です</span>
<p style="margin: 10px;"><b>${headerNames[6]}</b> 列では <b>${catToName[7]}</b> の色を示します：<br> 
<b>${fidToName[fidThreshold[6]]}</b>, <span style="color:rgb(131, 182, 239);"><b>${fidToName[fidThreshold[6]+1]}</b></span>, <span style="color:rgb(240, 230, 140);"><b>${fidToName[fidThreshold[6]+2]}</b></span>, <span style="color:rgb(239, 131, 131);"><b>${fidToName[fidThreshold[6]+3]}</b></span>, <span style="color:rgb(216, 143, 205);"><b>${fidToName[fidThreshold[6]+4]}</b></span></p>
<hr>
<p style="margin: 10px;">ポケモンを <span style="color:rgb(240, 230, 140); font-weight: bold;">ピン留め</span> する, <a href="https://wiki.pokerogue.net/start" target="_blank"><b>Wiki</b></a> を見る,<br>または <span style="color:${fidToColor(fidThreshold[7])[0]}; font-weight: bold;">色違い</span> を確認できます</p><p style="margin: 10px;">以下をクリックして詳細を表示：<br>
<span style="color:${col.wh}; font-weight: bold;">名前</span>, 
<span style="color:${fidToColor(fidThreshold[3])[0]}; font-weight: bold;">${headerNames[6]}</span>, 
<span style="color:${col.pu}; font-weight: bold;">${catToName[1]}</span>, 
<span style="color:${col.pu}; font-weight: bold;">${catToName[2]}</span></p>
<hr style="margin-bottom: 10px;">
<span style="color:rgb(145, 145, 145); font-size:11px">このサイトは Sandstorm によって多大な努力のもと作成されました。クッキーは保存しておらず, 個人データの収集も行っていません。画像とゲームデータは PokeRogue の GitHub から取得しています。すべてのアセットの著作権は元の制作者に帰属します。</span>
"""