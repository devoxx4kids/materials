;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-lambda-reader.ss" "lang")((modname gui-app) (read-case-sensitive #t) (teachpacks ((lib "image.rkt" "teachpack" "2htdp") (lib "universe.rkt" "teachpack" "2htdp"))) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ((lib "image.rkt" "teachpack" "2htdp") (lib "universe.rkt" "teachpack" "2htdp")))))
(require 2htdp/image)
(require 2htdp/universe)
(require 2htdp/planetcute)

(define background
  (rectangle 600 400 "solid" "gray"))

(define red-circle
  (lambda (diameter)
    (circle diameter "solid" "red")))

(check-expect (red-circle 32)
              (circle 32 "solid" "red"))

(define circle-on-background
  (lambda (diameter)
    (overlay (red-circle diameter) background)))

(check-expect (circle-on-background 32)
              (overlay
               (red-circle 32)
               background))

(define halve
  (lambda (world a-key) (/ world 2)))

(check-expect (halve 300 "space") 150)

(define my-gui-app
  (lambda (show-function)
    (big-bang
     0
     (on-tick add1)
     (to-draw show-function))))