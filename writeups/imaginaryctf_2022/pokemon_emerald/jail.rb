#!/usr/bin/env -S stdbuf -o0 -i0 ruby
code = gets.strip
# abcfjnrtuxy%{}_01234
code.each_char do |c|
  unless "jctf{any%_2uby_3xtr4ct10n}".include? c
    puts "NO!"
    exit
  end
end
puts eval(code)
