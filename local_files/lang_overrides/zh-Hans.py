headerNames = ['编号','图片','名称','属性','特性','蛋招式','费用',
               '全部','HP','攻击','防御','特攻','特防','速度']
altText = ['招式','标准','梦特','被动','搜索','威力','命中','PP',
           '添加到筛选','回忆蘑菇','闪光','蛋招式','稀有 蛋招式',
           '常见','超','高','学习器','等级','进化','蛋']
catToName = ['属性','特性','招式','世代','费用','蛋','模式',
             '进化','形态','环境','相关','变种闪光','标签']
infoText = ['每颗糖果的亲密度','被动','费用降低','兑换一颗蛋','梦特',
            '蛋 限定','宝宝 限定','悖论宝可梦','形态变化','环境','已选筛选',
            '## 个蛋后减少','通过等级','通过蛋','通过招式学习器']
biomeText = ['普通','罕见','稀有','非常稀有','极其稀有','Boss','普通','罕见','稀有','非常','极其','黎明','白天','黄昏','夜晚']
phrases = {
    'exclusive': '限定',
    'new': '新的',
    'tag': '属性',
    'theEnd': '终点',
    'fullyEvolved': '完全进化',
    'formBase': '基础',
    'formMega': '超级',
    'formNewMega': '新超级',
    'formGiga': '超极巨',
    'formTransformed': '变形',
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
    'spreadMoves': '范围招式', # 群体攻击
}
substitutions = [ # Text shortenings to make it fit in the UI
    ["超极巨化","超极巨"],
]
helpMenuText = [
'这是一个用于 PokeRogue 的<span style="color:rgb(140, 130, 240);">快速且强大的搜索</span>工具',
'使用 <span style="color:rgb(140, 130, 240);">搜索栏</span> 添加筛选条件：',
'组合多个筛选条件以获得所需结果',
'点击筛选逻辑切换“并且”或“任意”匹配方式',
'点击 <span style="color:rgb(140, 130, 240);">表头</span> 以排序结果：',
'<b>${headerNames[1]}</b> 列可以限制为异色形态',
'<b>${headerNames[4]}</b> 列可以限制为一个栏位：',
'主要特性', '${infoText[4]}', '${infoText[1]}',
'<b>${headerNames[5]}</b> 显示为 <b>${fidToName[fidThreshold[4]]}</b> 和 <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[4]+1]}</span>',
'点击表头可切换为<b>${infoText[9]}</b>',
'该列也会显示<b>已筛选的${altText[0]}/${infoText[9]}</b>',
'<b>${catToName[4]}</b> 列显示 <b>${catToName[5]}</b> 的颜色：',
'点击条目查看以下详细信息：',
'点击<b>${headerNames[2]}</b>查看完整招式表。',
'<b>${altText[5]}</b>的颜色表示<span style="color:${col.or}; font-weight: bold;">物理</span>或<span style="color:${col.bl}; font-weight: bold;">特殊</span>伤害',
'<b>${altText[6]}</b>的颜色表示<span style="color:${col.re}; font-weight: bold;">群体攻击</span>招式',
'本网站由 Sandstorm 创建，倾注了大量心血。我不存储任何 cookie, 也不收集任何个人数据。图片和游戏数据来自 PokeRogue 的 GitHub。所有素材版权归原作者所有。',
'游戏版本', '日期', '永久筛选条件',
]