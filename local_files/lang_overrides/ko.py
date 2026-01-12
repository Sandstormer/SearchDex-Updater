headerNames = ['번호','이로치','종','타입','특성','알기술','코스트','합계','HP','공격','방어','특공','특방','스핏']
altText = ['기술','일반 특성','숨겨진 특성','패시브 특성','검색','위력','명중률','PP','필터에 추가','기억버섯','진화계보','알 기술','레어 알 기술','일반','슈퍼','하이퍼','머신','레벨','진화','알']
catToName = ['타입','특성','기술','세대','코스트','성별','모드','알','색 다른 이로치','바이옴','진화계보','태그']
infoText = ['사탕당 친밀도','패시브','코스트 감소','알 구매하기','숨겨진 특성',
            '알 한정','베이비 포켓몬','패러독스 포켓몬','형태 변화','바이옴','선택 필터',
            '## 알 후 감소','레벨로','알로','기술머신으로']
biomeText = ['보통','드묾','레어','슈퍼 레어','하이퍼 레어','보스','보통','드묾','레어','슈퍼','하이퍼','새벽','낮','황혼','밤']
biomeLongText = [
    '<b><span style="color:rgb(131, 182, 239);">형태 변화</span>를 통해서만 얻을 수 있습니다.</b><br>',
    '<b>이 포켓몬은 <span style="color:rgb(143, 214, 154);">알 한정</span>입니다.</b><br>어떤 바이옴에서도 등장하지 않으며, 알 부화로만 획득할 수 있습니다.',
    '<b>이 포켓몬은 <span style="color:rgb(216, 143, 205);">베이비 포켓몬</span>입니다.</b><br>바이옴에서는 등장하지 않지만, 진화형을 만나면 해금됩니다.',
    '<b>이 <span style="color:rgb(239, 131, 131);">패러독스 포켓몬</span>은 <span style="color:rgb(143, 214, 154);">알 한정</span>입니다.</b><br>알로만 얻을 수 있지만, 이후 클래식 모드에서 포획할 수 있습니다.',
    '이 포켓몬은 <b><span style="color:rgb(239, 131, 131);">모든 다른 포켓몬</span></b>을 획득한 후에만 잡을 수 있습니다.<br>일반 알에서는 등장하지 않습니다.',
    '<b>이 형태는 획득할 수 없습니다.</b>',
]
warningText = [
    '색이 다른 포켓몬(이로치)만 사용할 수 있습니다.',
    '특성은 일반 특성으로만 제한됩니다.',
    '특성은 숨겨진 특성으로만 제한됩니다.',
    '특성은 패시브 특성으로만 제한됩니다.',
    '<b>필터와 검색어에 일치하는 포켓몬이 없습니다.</b><br>다른 필터를 추가하면 결과가 달라질 수 있습니다.',
    '<b>추천 항목을 클릭하면 필터가 적용됩니다.</b><br>필터 미리보기는 종족/타입/특성만 표시됩니다.',
    '<b>필터와 검색어에 일치하는 포켓몬이 없습니다.</b><br>다른 조합을 시도해 보세요.',
    '<b>필터에 일치하는 포켓몬이 없습니다.</b><br>필터를 제거하거나 연결 방식을 "OR"로 변경해 보세요.',
    '<b>검색어에 일치하는 포켓몬이나 필터가 없습니다.</b><br>철자를 확인하고 다시 시도해 주세요.',
    '클릭하여 사용 방법을 확인하세요.',
]
procToDesc = ["사용자 공격","사용자 방어","사용자 특수공격","사용자 특수방어","사용자 스피드","사용자 명중률","사용자 회피율", # [0-6]
    "공격","방어","특수공격","특수방어","스피드","명중률","회피율", # [7-13]
    "중독 부여","맹독 부여","잠듦 부여","얼음 부여","마비 부여","화상 부여","혼란 부여", # [14-20]
    "풀죽음","사용자 공/방/특공/특방/스피드","중독/마비/잠듦","화상/마비/얼음","스텔라 사용자 공/특공","데미지","우선도"] # [21-27]
tagToDesc = [
    "대상: 무작위 적",
    "대상: 모든 적",
    "대상: 전체 필드",
    "급소율 높음",
    "급소 확정",
    "사용자 급소율 +2",
    "사용자 공격 최대",
    "HP 33% 소모",
    "HP 50% 소모",
    "반동 HP 50%",
    "반동 피해의 50%",
    "반동 피해의 33%",
    "반동 피해의 25%",
    "30% 확률 2배 피해",
    "미사용",
    "가한 피해의 100% 회복",
    "가한 피해의 75% 회복",
    "가한 피해의 50% 회복",
    "상대 공격력만큼 회복",
    "상태 이상 회복",
    "수면 회복",
    "얼음 회복",
    "화상 회복",
    "풀/방진 특성 무효",
    "풀 타입에 씨뿌리기 불가",
    "힐링시프트 특성 발동",
    "춤꾼 특성 발동",
    "바람타기 특성 발동",
    "예리함으로 강화",
    "철주먹으로 강화",
    "메가런처으로 강화",
    "옹골찬턱으로 강화",
    "이판사판으로 강화",
    "방탄 특성에 무효",
    "습기 특성에 방해됨",
    "소리 기반 기술",
    "대타출동 무시",
    "특성 무시",
    "방어/지키기 무시",
    "사용자 교체",
    "상대 교체",
    "2회 공격",
    "3회 공격",
    "10회 공격",
    "2~5회 공격",
    "2~3턴 동안 반복",
    "장애물 제거",
    "상대를 가두고 피해",
    "억제 불가",
    "대체 불가",
    "무시 불가",
    "재지정 불가",
    "반사 불가",
    "비 오는 날씨에서 항상 명중",
    "사용자 교체 불가",
    "상대 교체 불가",
    "일격 기술",
    "보스전에서 수정됨",
    "보스에게 효과 없음",
    "더블배틀코롱 특성",
    "접촉 기술",
    "부분 구현됨",
    "미구현",
]
helpMenuText = """
<b>포켓로그용 <span style="color:rgb(140, 130, 240);">빠르고 강력한 검색</span> 사이트입니다.</b>
<hr>
<p style="margin: 10px; font-weight: bold;"><span style="color:rgb(140, 130, 240);">검색 창</span> 으로 필터를 추가할 수 있습니다:<br></p>
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
여러 필터를 조합하여 원하는 결과를 얻으세요. <br>
<span style="color:rgb(145, 145, 145);">필터를 클릭하여 둘 중 하나와 일치시킬 수 있습니다.</span>
<hr>
<p style="margin: 10px; font-weight: bold;">결과를 정렬하려면 <span style="color:rgb(140, 130, 240);">헤더</span> 를 클릭하세요:</p>
<b>${headerNames[1]}</b> 열은 이로치 포켓몬으로만 제한할 수 있어요.
<p style="margin: 10px;"><b>${headerNames[4]}</b> 열은 특정 슬롯으로 제한할 수 있습니다:<br>
<b>주요 특성</b>, 
<span style="color:rgb(240, 230, 140); font-weight: bold;">숨겨진 특성</span>, 또는 
<span style="color:rgb(140, 130, 240); font-weight: bold;">패시브</span></p>
<b>${headerNames[5]}</b>는 <b>${fidToName[fidThreshold[6]]}</b> 및 <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[6]+1]}</span>로 표시됩니다.<br> 
<span style="color:rgb(145, 145, 145);">필터링된 기술의 출처도 표시할 수 있습니다.</span>
<p style="margin: 10px;"><b>${headerNames[6]}</b> 열은 <b>${catToName[7]}</b>의 색상을 표시합니다:<br> 
<b>${fidToName[fidThreshold[6]]}</b>, <span style="color:rgb(131, 182, 239);"><b>${fidToName[fidThreshold[6]+1]}</b></span>, <span style="color:rgb(240, 230, 140);"><b>${fidToName[fidThreshold[6]+2]}</b></span>, <span style="color:rgb(239, 131, 131);"><b>${fidToName[fidThreshold[6]+3]}</b></span>, <span style="color:rgb(216, 143, 205);"><b>${fidToName[fidThreshold[6]+4]}</b></span></p>
<hr>
<p style="margin: 10px;">포켓몬을 <span style="color:rgb(240, 230, 140); font-weight: bold;">고정</span> 하거나, <a href="https://wiki.pokerogue.net/start" target="_blank"><b>위키</b></a> 또는 <span style="color:${fidToColor(fidThreshold[7])[0]}; font-weight: bold;">이로치</span> 확인.</p>
<p style="margin: 10px;">클릭하면
<span style="color:rgb(140, 130, 240); font-weight: bold;">${catToName[1]}</span> 또는 
<span style="color:rgb(140, 130, 240); font-weight: bold;">${catToName[2]}</span> 의 설명을 볼 수 있습니다.</p>
<hr style="margin-bottom: 10px;">
<span style="color:rgb(145, 145, 145); font-size:11px">이 사이트는 Sandstorm 이 만들었으며, Misdreavus 가 번역을 도왔습니다. 쿠키를 저장하거나 개인 데이터를 수집하지 않습니다. 이미지와 게임 데이터는 PokeRogue GitHub 에서 제공되며, 자산 권리는 원 제작자에게 있습니다.</span>
"""