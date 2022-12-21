def clean_string_for_lua(string):
    return string.replace("'", "").replace('"', "")

def get_full_lua(spawning_lua:str):
    return f"""\
function onLoad()
    local has_spawned = false
end

function onDrop(player_color)
    if has_spawned then
        return
    end
    has_spawned = true  
    spawnSelf()
end

function spawnSelf()
    {spawning_lua}
end
"""

def scale_size(size):
    if size == 0.25:
        return size
    else:
        return size * 0.4