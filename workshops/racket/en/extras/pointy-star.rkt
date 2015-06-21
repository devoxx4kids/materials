#lang racket

(require 2htdp/image)

(define RADIUS 8)
(define RED 255)

(define make-red
  (lambda (r) (make-color r 0 0)))

(define make-star
  (lambda (level)
    (radial-star
     6
     (+ RADIUS (* 8 level))
     64
     "solid"
     (make-red
      (- RED (* level 20))))))

(define make-a-star
  (overlay
   (make-star 0)
   (make-star 1)
   (make-star 2)
   (make-star 3)
   (make-star 4)
   (make-star 5)
   (make-star 6)))

make-a-star