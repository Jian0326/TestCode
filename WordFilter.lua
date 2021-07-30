--- 使用lua5.3
---@class WordFilter
local WordFilter = class("service.common.word_filter")

function WordFilter:ctor()
    self.wordTree = {}
    -- 这里自行添加屏蔽词
    local map     = this.sheetdata("wordfilter", "key")
    for key, _ in pairs(map) do
        self:add_wold_filter(self.wordTree, key);
    end
end

-- 添加屏蔽词
---@param tree table<number,{}>
---@param word  string
function WordFilter:add_wold_filter(tree, word)

    local function add_code(map, code, isLast)
        if not map[code] then map[code] = {} end
        if isLast then map[code].last = true end
        return map[code]
    end

    repeat
        if not word then break end
        local len = utf8.len(word)
        if len <= 0 then break end
        local temp = tree
        local idx  = 1 --统计循环次数
        for _, code in utf8.codes(word) do
            temp = add_code(temp, code, idx == len)
            idx  = idx + 1
        end
    until true
end

function WordFilter:check_word_filter(word)

    local function is_filter(map, code)
        if not map[code] then return false end
        return map[code]
    end

    local function check(codes, tree, begIdx, retVal)
        local len  = #codes
        local temp = tree
        for i, code in ipairs(codes) do
            local ret = is_filter(temp, code)
            if not ret and i == len then break end
            if not ret then
                check(table.sub(codes, i, len), self.wordTree, begIdx + i - 1, retVal)
                break
            end
            if not ret.last then
                temp = ret
            else
                if i == len or (i < len and not ret[codes[i + 1]]) then
                    table.insert(retVal, { begIdx, begIdx + i - 1 })
                    check(table.sub(codes, i + 1, len), self.wordTree, begIdx + i - 1, retVal)
                    break
                end
                temp = ret
            end
        end
    end

    local retVal = {}
    local codes  = {}
    repeat
        if not word then break end
        local len = utf8.len(word)
        if len <= 0 then break end
        for _, code in utf8.codes(word) do
            table.insert(codes, code)
        end
        check(codes, self.wordTree, 1, retVal)
    until true
    return retVal, codes
end

function WordFilter:replace_word_filter(word, replace)
    local filter, codes = self:check_word_filter(word)
    if #filter <= 0 then return word end
    for i, list in ipairs(filter) do
        for j = list[1], list[2] do
            codes[j] = string.byte(replace)
        end
    end
    return utf8.char(table.unpack(codes))
end
