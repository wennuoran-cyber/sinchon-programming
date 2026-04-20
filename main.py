# --- 主角状态 (Player State) ---
# 文档要求：记录位置和饥饿感 [cite: 13, 14]
player_state = {
    "location": "延世大学前公交站",  
    "status": "肚子饿"
}

# --- 环境状态 (Environment State) ---
# 文档要求：记录当前时间为 11点 [cite: 17]
world_state = {
    "current_time": 11
}

print(f"目前位置: {player_state['location']}")
print(f"当前时间: {world_state['current_time']}点")