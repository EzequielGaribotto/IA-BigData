-- Sizes table columns by their content, not by the number of dashes in the Markdown source.
local function longest_word_and_text(cell)
  local text = pandoc.utils.stringify(cell.contents)
  local word = 0
  for w in text:gmatch("%S+") do word = math.max(word, utf8.len(w) or #w) end
  return word, utf8.len(text) or #text
end

function Table(tbl)
  local n = #tbl.colspecs
  local words, texts = {}, {}
  for c = 1, n do words[c], texts[c] = 1, 1 end
  local function scan(rows)
    for _, row in ipairs(rows) do
      for c, cell in ipairs(row.cells) do
        local word, text = longest_word_and_text(cell)
        words[c] = math.max(words[c], word)
        texts[c] = math.max(texts[c], text)
      end
    end
  end
  scan(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do scan(body.body) end
  -- Square root: long text columns get more room, without starving the short ones
  local weights, total = {}, 0
  for c = 1, n do
    weights[c] = math.max(math.sqrt(texts[c]), words[c] * 0.45)
    total = total + weights[c]
  end
  for c = 1, n do
    tbl.colspecs[c] = {tbl.colspecs[c][1], weights[c] / total}
  end
  return tbl
end
