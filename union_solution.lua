function find_signal(value, past,future)
   signal = (value + 1) % 100
   for i = 1, #past do
      hat = past[i]
      if hat == signal then
         return find_signal(signal, past, future)
      end
   end
   for i=1, #future do
      hat = future[i]
      if hat == signal then
         return find_signal(signal, past, future)
      end
   end
   return signal
end

function find_value(signal, past,future)
   value = (signal - 1) % 100
   for i = 1, #past do
      hat = past[i]
      if hat == value then
         return find_value(value, past, future)
      end
   end
   for i=1, #future do
      hat = future[i]
      if hat == value then
         return find_value(value, past, future)
      end
   end
   return value
end

function Worker(previous_calls,future_lineup)
  -- Put your worker strategy here
  -- previous_calls is an array of the calls by the previous workers
  -- future_lineup is an array of the hats that can be seen ahead by this worker

   if #previous_calls < 49 then
      return find_signal(future_lineup[1+49], previous_calls, future_lineup)
   elseif #previous_calls == 49 then
      return find_signal(0,previous_calls, future_lineup)
   else
      return find_value(previous_calls[#previous_calls-49], previous_calls, future_lineup)
   end
  
end

