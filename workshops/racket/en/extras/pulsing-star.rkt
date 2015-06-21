#lang racket

(require 2htdp/image)
(require 2htdp/universe)

(define WIDTH 400)
(define HEIGHT 200)
(define background
  (rectangle
   WIDTH
   HEIGHT
   "solid"
   "black"))
(define PERIOD 70)
(define COLOR "red")

(define make-star
  (lambda (period color frame)
    (radial-star
     8
     2
     (remainder frame period)
     "solid"
     color)))

(define make-scene
        (lambda (frame)
            (place-image
             (make-star PERIOD COLOR frame)
             (* 0.25 WIDTH)
             (* 0.30 HEIGHT)
             background)))

(animate make-scene)