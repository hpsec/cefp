; (c) Copyright 2013 Hewlett-Packard Development Company, L.P.

; Licensed under the MIT License.

; Permission is hereby granted, free of charge, to any person obtaining a
; copy of this software and associated documentation files (the
; "Software"), to deal in the Software without restriction, including
; without limitation the rights to use, copy, modify, merge, publish,
; distribute, sublicense, and/or sell copies of the Software, and to permit
; persons to whom the Software is furnished to do so, subject to the
; following conditions:

; The above copyright notice and this permission notice shall be included
; in all copies or substantial portions of the Software.

; Author: Jeremy Kelley <jeremy.kelley@hp.com> @nod


;;; Parses cef type input into a native hash.
;;; for now, sort of ignores the key type. ambiguity isn't a bad thing.

(ns cefp.cefp
	(:use [clojure.string :only (split)])
	)

; CEF connector prefixes with pipe delimited before getting to key value data
(defn find-kv [cefs]
    (last (split cefs #"\|" 8))
    )

(defn keyval [s]
    (map
        #(take-last 2 %)
        (map #(re-find #"(\w+)=(.*)" %)  (split s #" (?=\w+=)"))
        )
    )

; convenience: keywords to symbols
(defn symval [k v] [(keyword k) v])

; accepts key val pairs and returns dict
(defn cef-parse [cefkv]
    (into {} (map (fn [[k v]] (symval k v)) (keyval cefkv)))
    )

; accepts line from Syslog CEF and returns dict
(defn cef-from-line [line]
    (cef-parse (find-kv line))
    )

(defn -main
	[]
	(println (split "k=v mydog=the cat.is-a beast" #" (?=\w+=)"))
	)
