#lang racket

(require 2htdp/image)
(require 2htdp/universe)

(define SQUARE_COLOR "chartreuse")

(define background
  (rectangle 1000 600 "solid" "black"))

(define make-a-square
  (lambda (w)
    (overlay
     (square w "outline" "black")
     (square w "solid" SQUARE_COLOR))))

(define spiral
  (lambda (s)
    (rotate
     90
     (crop
      0 0 (image-width s) (image-width s)
      (overlay/align
       "left"
       "top"
       (circle (image-width s) "outline" "red")
       s)))))

(define unit-square
  (spiral (make-a-square 5)))

(define make-square
  (lambda (s)
    (beside  
     (spiral (make-a-square (image-width s)))
     (rotate 90 s))))

(define fib-square
  (lambda (x)
    (if
     (= x 0)
     unit-square
     (make-square (fib-square (- x 1))))))

(big-bang
 (fib-square 0)
 (state true)
 (on-key (lambda (w k) (make-square w)))
 (to-draw (lambda (x) (overlay x background))))
