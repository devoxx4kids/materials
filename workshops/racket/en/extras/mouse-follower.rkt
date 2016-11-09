#lang racket

(require 2htdp/image)
(require 2htdp/universe)

(define CRAYON
  (circle 10 "solid" "pink"))

(define background
  (rectangle 500 300 "solid" "black"))

(define (follow-mouse w x y event)
  (place-image
   CRAYON
   x
   y
   w))

(define (the-image x) x)

(define (clear w) background)

(big-bang
 background
 (on-tick clear)
 (state true)
 (on-mouse follow-mouse)
 (to-draw the-image)
 (check-with image?))