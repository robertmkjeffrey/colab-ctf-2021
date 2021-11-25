function Worker(previous_calls,future_lineup)
  -- Put your worker strategy here
  -- previous_calls is an array of the calls by the previous workers
  -- future_lineup is an array of the hats that can be seen ahead by this worker
  hash = 0
  for i=1, #future_lineup do
    hash = hash + future_lineup[i]
    hash = hash % 4
  end
  if previous_calls[1] == nil then
    return (4-hash) % 4
  end
  
  for i=1, #previous_calls do
    hash = hash + previous_calls[i]
    hash = hash % 4
  end

  return (4-hash) % 4
end

