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