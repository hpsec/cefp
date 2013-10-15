(ns cefp.test.core
  (:use [cefp.cefp :only (cef-parse find-kv keyval symval)])
  (:use [clojure.test]))

(deftest test-find-kv
    (is (= "k=v" (find-kv "|||||||k=v")))
    (is (= "ka=v k2=v\\|" (find-kv "|||||||ka=v k2=v\\|")))
    (is (= "kb=v\\|k3=4" (find-kv "|||||||kb=v\\|k3=4")))
	)

(deftest test-keyval
	(is (= [["k" "v"]] (keyval "k=v")))
	(is (= [["k" "v"] ["x" "y"]] (keyval "k=v x=y")))
	(is (= [["k" "v"] ["x" "y"] ["somedog" "mycat"]]
		(keyval "k=v x=y somedog=mycat")))
	(is (= [["someKey" "this will be a dooze\\=yep"]]
		(keyval "someKey=this will be a dooze\\=yep")))
	(is (= [["x" "y"] ["someKey" "this will be a dooze\\=yep"]]
		(keyval "x=y someKey=this will be a dooze\\=yep")))
	(is (=
		[["eventId" "757012"] ["mrt" "1122339894099"]
			["categorySignificance" "/Normal"]]
		(keyval "eventId=757012 mrt=1122339894099 categorySignificance=/Normal")
		))
	)

(deftest test-symval
	(is (= [:k "v"] (symval "k" "v")))
	)

(deftest test-cef-parse
	(is (= {:k "v"} (cef-parse "|||||||k=v")))
	)
