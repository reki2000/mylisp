;(define loop (fn (n) (if (eq? n 0) 100 (loop (- n 1)))))
;(define sum (fn (n) (if (eq? n 0) 0 (+ n (sum (- n 1))))))

; samples
(define fib (fn (n) (cond ((eq? n 0) 0) ((eq? n 1) 1) (1 (+ (fib (- n 1)) (fib (- n 2))))) ))
(define factorial (fn (n) (cond ((eq? n 1) 1) (1 (* n (factorial (- n 1)))))))
