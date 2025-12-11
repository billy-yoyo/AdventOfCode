ReadFileLines ← ⊜□≠ , @\n ▽ ≠ @\r . &fras
Lines ← ReadFileLines "puzzle"

# ??? <- lines
ParseLines ← ⍥(|3
  # lines stack prefix
  !∶ ⊡ [# line lines stack prefix
        (|4.3 ?(⊙⊙(⍜⇌ (↘ + 1 ⊗ @/ .))) (⊙⊙(⊂⊂ ∶"/" ∶) ⊙∶ ∶) ≅ ".." ↙ 2 . ↘ 5)
        (|4.3 ∘;)
        (|4.3 ∘;)
        (|4.3 ⊙(⊂∶) ∶ ⊂□⊂∶ ⊙∶ ⊙⊙∶ ⊙⊙⊙∶ ⊙⊙⊙⊙. ↘+1⊗@ ∶ □parse↙⊗@ .)] ⊗ ["$ cd"
                                                                      "$ ls"
                                                                      "dir "] ↙ 4 .
  ⊙(↘ 1)
  ⊡ 0 .
  ⎋ = 0 ⧻ .
)∞ []∶""∶

ParseLines Lines
