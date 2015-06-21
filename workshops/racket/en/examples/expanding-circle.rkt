;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-lambda-reader.ss" "lang")((modname expanding-circle) (read-case-sensitive #t) (teachpacks ((lib "image.rkt" "teachpack" "2htdp") (lib "universe.rkt" "teachpack" "2htdp"))) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ((lib "image.rkt" "teachpack" "2htdp") (lib "universe.rkt" "teachpack" "2htdp")))))
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