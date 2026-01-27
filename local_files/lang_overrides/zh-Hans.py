headerNames = ['编号','闪光','名称','属性','特性','蛋招式','费用','全部','HP','攻击','防御','特攻','特防','速度']
altText = ['招式','标准','梦特','被动','搜索','威力','命中','PP','添加到筛选','回忆蘑菇','进化','蛋招式','稀有 蛋招式','常见','超','高','学习器','等级','进化','蛋']
catToName = ['属性','特性','招式','世代','费用','性别','模式','蛋','变种闪光','环境','相关于','标签']
infoText = ['每颗糖果的亲密度','被动','费用降低','兑换一颗蛋','梦特',
            '蛋 限定','宝宝 限定','悖论宝可梦','形态变化','环境','已选筛选',
            '## 个蛋后减少','通过等级','通过蛋','通过招式学习器']
biomeText = ['普通','罕见','稀有','非常稀有','极其稀有','Boss','普通','罕见','稀有','非常','极其','黎明','白天','黄昏','夜晚']
phrases = {
    'exclusive': '限定',
    'new': '新的',
    'tag': '属性',
    'theEnd': '终点',
    'lureAbility': '诱导特性',
    'ignoresAbilities': '无视特性',
    'electricImmunity': '免疫电',
    'fireImmunity': '免疫火',
    'waterImmunity': '免疫水',
    'rainAbility': '雨天特性',
    'sandAbility': '沙暴特性',
    'snowAbility': '雪天特性',
    'sunAbility': '晴天特性',
    'targetSwitchesOut': '迫使对手替换',
    'spreadMoves': '范围招式',
}
helpMenuText = """
<b>这是一个用于 PokeRogue 的<span style="color:rgb(140, 130, 240);">快速且强大的搜索</span>工具</b>
<hr>
<p style="margin: 10px; font-weight: bold;">使用 <span style="color:rgb(140, 130, 240);">搜索栏</span> 添加筛选条件：<br></p>
<p style="margin: 10px; font-weight: bold;"><span style="color:${typeColors[9]};">${catToName[0]}</span>, 
<span style="color:${fidToColor(fidThreshold[0])[0]};">${catToName[1]}</span>,
<span style="color:${fidToColor(fidThreshold[1])[0]};">${catToName[2]}</span>,
<span style="color:${fidToColor(fidThreshold[2])[0]};">${catToName[3]}</span>,
<span style="color:${fidToColor(fidThreshold[3])[0]};">${catToName[4]}</span>,
<span style="color:${fidToColor(fidThreshold[4])[0]};">${catToName[5]}</span>,<br>
<span style="color:${fidToColor(fidThreshold[5])[1]};">${catToName[6]}</span>,
<span style="color:${eggTierColors(2)};">${catToName[7]}</span>,
<span style="color:${fidToColor(fidThreshold[7])[0]};">${headerNames[1]}</span>, 
<span style="color:${fidToColor(fidThreshold[8])[0]};">${catToName[9]}</span></p>
组合多个筛选条件以获得所需结果 <br>
<span style="color:rgb(145, 145, 145);">点击筛选逻辑切换“并且”或“任意”匹配方式</span>
<hr>
<p style="margin: 10px; font-weight: bold;">点击 <span style="color:rgb(140, 130, 240);">表头</span> 以排序结果</p>
<b>${headerNames[1]}</b> 列可以限制为异色形态
<p style="margin: 10px;"><b>${headerNames[4]}</b> 列可以限制为一个栏位：<br>  
<b>主要特性</b>,
<span style="color:rgb(240, 230, 140); font-weight: bold;">${infoText[4]}</span>, 
<span style="color:rgb(140, 130, 240); font-weight: bold;">${infoText[1]}</span></p>
<b>${headerNames[5]}</b> 显示为 <b>${fidToName[fidThreshold[6]]}</b> 和 <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[6]+1]}</span><br>
<span style="color:rgb(145, 145, 145);">还可以显示筛选招式的来源</span>  
<p style="margin: 10px;"><b>${headerNames[6]}</b> 列显示 <b>${catToName[7]}</b> 的颜色：<br>
<b>${fidToName[fidThreshold[6]]}</b>, <span style="color:rgb(131, 182, 239);"><b>${fidToName[fidThreshold[6]+1]}</b></span>, <span style="color:rgb(240, 230, 140);"><b>${fidToName[fidThreshold[6]+2]}</b></span>, <span style="color:rgb(239, 131, 131);"><b>${fidToName[fidThreshold[6]+3]}</b></span>, <span style="color:rgb(216, 143, 205);"><b>${fidToName[fidThreshold[6]+4]}</b></span></p>
<hr><p style="margin: 10px;">点击<span style="color:rgb(240, 230, 140);">固定</span>一只宝可梦, 或查看<a href="https://wiki.pokerogue.net/start" target="_blank"><b>维基</b></a>, 或查看<span style="color:${fidToColor(fidThreshold[7])[0]};">异色形态</span></p>
<p style="margin: 10px;">点击 
<span style="color:${col.wh}; font-weight: bold;">名字</span>, 
<span style="color:${fidToColor(fidThreshold[3])[0]}; font-weight: bold;">${headerNames[6]}</span>, 
<span style="color:${col.pu}; font-weight: bold;">${catToName[1]}</span>, 
<span style="color:${col.pu}; font-weight: bold;">${catToName[2]}</span> 查看详细信息</p>
<hr style="margin-bottom: 10px;">
<span style="color:rgb(145, 145, 145); font-size:11px">本网站由 Sandstorm 创建，倾注了大量心血。我不存储任何 cookie, 也不收集任何个人数据。图片和游戏数据来自 PokeRogue 的 GitHub。所有素材版权归原作者所有。</span>
"""