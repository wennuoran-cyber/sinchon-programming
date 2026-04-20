import os
import pickle

# ====================== 1. 기본 설정 ======================
# 지도 좌표 (행, 열)
map_data = [
    ["종합관", "본관", "경영관", "노천극장", "새천년관", "이윤재관"],
    ["백양관", "백양로5", "대강당", "음악관", "알렌관", "ABMRC"],
    ["중앙도서관", "독수리상", "학생회관", "루스채플", "재활병원", "치과대학"],
    ["체육관", "백양로3", "공터2", "광혜원", "어린이병원", "세브란스"],
    ["공학관", "백양로2", "백주년기념관", "안과병원", "제중관", ""],
    ["공학원", "백양로1", "공터1", "암병원", "의과대학", ""],
    ["연대앞 버스정류장", "정문", "스타벅스", "세브란스 버스정류장", "", ""]
]

# 위치 좌표 찾기
def get_pos(place_name):
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if map_data[i][j] == place_name:
                return (i, j)
    return (-1, -1)

# 이웃 위치 찾기
def get_neighbors(pos):
    i, j = pos
    res = {"동": "막힘", "서": "막힘", "남": "막힘", "북": "막힘"}
    rows = len(map_data)
    cols = len(map_data[0])
    if j + 1 < cols and map_data[i][j+1]:
        res["동"] = map_data[i][j+1]
    if j - 1 >= 0 and map_data[i][j-1]:
        res["서"] = map_data[i][j-1]
    if i + 1 < rows and map_data[i+1][j]:
        res["남"] = map_data[i+1][j]
    if i - 1 >= 0 and map_data[i-1][j]:
        res["북"] = map_data[i-1][j]
    return res

# 이벤트 불러오기
with open("events.pkl", "rb") as f:
    event_data = pickle.load(f)
events = event_data["events"]
answers = event_data["answers"]

# ====================== 2. 플레이어 클래스 ======================
class Player:
    def __init__(self):
        self.hp = 10.0
        self.money = 10000
        self.place = "연대앞 버스정류장"
        self.bag = {"두쫀쿠": 0, "카페라떼": 0}
        self.quests = []
        self.done_quests = []

    def move(self, direction):
        i, j = get_pos(self.place)
        ni, nj = i, j
        if direction == "동": nj += 1
        elif direction == "서": nj -= 1
        elif direction == "남": ni += 1
        elif direction == "북": ni -= 1
        rows = len(map_data)
        cols = len(map_data[0])
        if 0 <= ni < rows and 0 <= nj < cols and map_data[ni][nj]:
            old = self.place
            self.place = map_data[ni][nj]
            if difficulty == "쉬움": self.hp -= 0.5
            elif difficulty == "어려움": self.hp -= 2
            else: self.hp -= 1
            return True
        else:
            return False

    def status(self):
        pos = get_pos(self.place)
        nei = get_neighbors(pos)
        s = f"[계좌 잔액: {self.money}원]\n[HP: {self.hp}]\n[현재위치: {self.place}]"
        s += f"\n동서남북: {nei['동']}, {nei['서']}, {nei['남']}, {nei['북']}"
        return s

# ====================== 3. 상점 / 퀘스트 ======================
def buy(p):
    place = p.place
    menu = {}
    if place == "학생회관":
        menu = {1: ("두쫀쿠", 5000, 10), 2: ("카페라떼", 3000, 5)}
    elif place in ["스타벅스", "ABMRC"]:
        menu = {1: ("두쫀쿠", 4000, 10), 2: ("카페라떼", 2000, 5)}
    else:
        return "여기서는 구매할 수 없습니다."
    print("1) 두쫀쿠\n2) 카페라떼\n3) 종료")
    c = input("선택: ")
    if c == "3": return "구매 종료"
    if c not in ["1", "2"]: return "잘못된 선택"
    idx = int(c)
    name, price, hp = menu[idx]
    if p.money < price: return "잔액 부족"
    p.money -= price
    p.bag[name] += 1
    return f"{name} 구매 완료! 가방에 추가"

def sell(p):
    if p.bag["두쫀쿠"] == 0 and p.bag["카페라떼"] == 0:
        return "팔 물건 없음"
    print("1) 두쫀쿠\n2) 카페라떼\n3) 종료")
    c = input("선택: ")
    if c == "3": return "판매 종료"
    if c not in ["1", "2"]: return "잘못된 선택"
    if c == "1" and p.bag["두쫀쫀"] > 0:
        p.bag["두쫀쿠"] -= 1
        p.money += 6000
        return "두쫀쿠 판매 완료"
    if c == "2" and p.bag["카페라떼"] > 0:
        p.bag["카페라떼"] -= 1
        p.money += 3000
        return "카페라떼 판매 완료"
    return "보유 수량 부족"

def quest(p):
    if p.place == "정문" and "기본미션" not in p.quests:
        p.quests.append("기본미션")
        return "독수리상에서 미션 받으러 가세요!"
    if p.place == "독수리상":
        if "부조리" not in p.quests:
            p.quests.append("부조리")
        if "위생" not in p.quests:
            p.quests.append("위생")
        return "미션 수락: 부조리 수사, 위생사건 수사"
    if p.place == "본관" and "부조리" in p.quests:
        ans = input("부조리 장소는? ")
        if ans == answers["교내 부조리 수사"]:
            p.quests.remove("부조리")
            p.done_quests.append("부조리")
            return "부조리 미션 완료!"
    if p.place == "세브란스" and "위생" in p.quests:
        ans = input("식중독 원인 장소는? ")
        if ans == answers["교내 위생사건 수사"]:
            p.quests.remove("위생")
            p.done_quests.append("위생")
            return "위생 미션 완료!"
    return "미션 관련 없음"

# ====================== 4. 저장 / 불러오기 ======================
def save_game(p, diff, inputs):
    data = {
        "player": p.__dict__,
        "difficulty": diff,
        "inputs": inputs
    }
    with open("save.pkl", "wb") as f:
        pickle.dump(data, f)
    return "저장 완료!"

def load_game():
    with open("save.pkl", "rb") as f:
        data = pickle.load(f)
    p = Player()
    p.__dict__ = data["player"]
    return p, data["difficulty"], data["inputs"]

# ====================== 5. 메인 실행 ======================
if __name__ == "__main__":
    player = Player()
    difficulty = "보통"
    input_log = []
    output_log = []
    print("=== 연세대학교 텍스트 게임 ===")
    print("명령어: 동/서/남/북 / 상태 / 가방 / 구매 / 판매 / 미션 / 저장 / 불러오기 / 종료")

    while True:
        cmd = input("명령: ")
        input_log.append(cmd)
        res = ""

        if cmd == "종료": break
        elif cmd in ["동", "서", "남", "북"]:
            ok = player.move(cmd)
            if ok:
                res = f"{player.place}로 이동!"
                if player.place in events:
                    res += "\n" + events[player.place]
            else:
                res = "그 방향은 막혔어."
        elif cmd == "상태":
            res = player.status()
        elif cmd == "가방":
            res = f"가방: {player.bag}"
        elif cmd == "구매":
            res = buy(player)
        elif cmd == "판매":
            res = sell(player)
        elif cmd == "미션":
            res = quest(player)
        elif cmd == "저장":
            res = save_game(player, difficulty, input_log)
        elif cmd == "불러오기":
            player, difficulty, input_log = load_game()
            res = "불러오기 완료!"

        print(res)
        output_log.append(res)

    # 입출력 기록 저장
    with open("player_input.txt", "w", encoding="utf-8") as f:
        for i, line in enumerate(input_log, 1):
            f.write(f"[{i}] {line}\n")
    with open("game_output.txt", "w", encoding="utf-8") as f:
        for i, line in enumerate(output_log, 1):
            f.write(f"[{i}] {line}\n")

    print("게임 종료! 기록 저장 완료")