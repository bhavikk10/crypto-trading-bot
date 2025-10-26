(ns crypto.api.http
  (:require [ring.adapter.jetty :as jetty]
            [ring.middleware.json :as json]
            [ring.middleware.cors :as cors]
            [ring.util.response :as response]
            [compojure.core :refer [defroutes GET POST]]
            [compojure.route :as route]
            [crypto.infra.redis :as redis]
            [crypto.infra.config :refer [get-config]]
            [taoensso.timbre :as timbre :refer [info error]]
            [clojure.data.json :as json]
            [mount.core :refer [defstate]])
  (:import [java.time Instant]))

;; HTTP API to expose Clojure crypto data to Python FastAPI backend

(defn get-redis-data [key]
  "Get data from Redis with error handling"
  (try
    (redis/redis* (car/get key))
    (catch Exception e
      (error e "Redis error for key" key)
      nil)))

(defn get-redis-list [key limit]
  "Get list data from Redis"
  (try
    (redis/redis* (car/lrange key (- limit) -1))
    (catch Exception e
      (error e "Redis list error for key" key)
      [])))

(defn format-price-response [data]
  "Format price data for API response"
  (if data
    (let [parsed (json/read-str data)]
      {:symbol (get parsed "symbol")
       :price (Double/parseDouble (get parsed "price"))
       :timestamp (.toString (Instant/now))
       :source "clojure-gdax"})
    {:error "No price data available"}))

(defn format-history-response [history-data]
  "Format historical data for API response"
  (mapv (fn [entry]
          (let [parsed (json/read-str entry)]
            {:timestamp (get parsed "timestamp")
             :open (Double/parseDouble (get parsed "open"))
             :high (Double/parseDouble (get parsed "high"))
             :low (Double/parseDouble (get parsed "low"))
             :close (Double/parseDouble (get parsed "close"))
             :volume (Double/parseDouble (get parsed "volume"))}))
        history-data))

(defn get-gdax-price [product-id]
  "Get GDAX price data"
  (let [price-key (str "gdax:price:" product-id)
        price-data (get-redis-data price-key)]
    (format-price-response price-data)))

(defn get-gdax-history [product-id limit]
  "Get GDAX historical data"
  (let [history-key (str "gdax:history:" product-id)
        history-data (get-redis-list history-key limit)]
    (format-history-response history-data)))

(defn get-binance-price [symbol]
  "Get Binance price data"
  (let [price-key (str "binance:price:" symbol)
        price-data (get-redis-data price-key)]
    (if price-data
      (let [parsed (json/read-str price-data)]
        {:symbol symbol
         :price (Double/parseDouble (get parsed "price"))
         :timestamp (.toString (Instant/now))
         :source "clojure-binance"})
      {:error "No Binance price data available"})))

(defn get-twilio-alerts [limit]
  "Get Twilio alerts"
  (let [alerts-key "twilio:alerts"
        alerts-data (get-redis-list alerts-key limit)]
    (mapv (fn [alert]
            (json/read-str alert))
          alerts-data)))

(defn get-system-status []
  "Get system status"
  (try
    (let [redis-info (redis/redis* (car/info))
          gdax-keys (redis/redis* (car/keys "gdax:*"))
          binance-keys (redis/redis* (car/keys "binance:*"))
          twilio-keys (redis/redis* (car/keys "twilio:*"))]
      {:clojure_system {:redis_connected true
                        :redis_info redis-info
                        :available_data {:gdax (> (count gdax-keys) 0)
                                         :binance (> (count binance-keys) 0)
                                         :twilio (> (count twilio-keys) 0)}}
       :timestamp (.toString (Instant/now))})
    (catch Exception e
      (error e "Error getting system status")
      {:clojure_system {:redis_connected false
                        :error (.getMessage e)}
       :timestamp (.toString (Instant/now))})))

;; API Routes
(defroutes api-routes
  ;; Health check
  (GET "/health" []
    (response/response {:status "ok"
                        :service "crypto-clojure-api"
                        :timestamp (.toString (Instant/now))}))
  
  ;; GDAX endpoints
  (GET "/gdax/price/:product-id" [product-id]
    (response/response (get-gdax-price product-id)))
  
  (GET "/gdax/history/:product-id" [product-id]
    (response/response (get-gdax-history product-id 100)))
  
  (GET "/gdax/history/:product-id/:limit" [product-id limit]
    (response/response (get-gdax-history product-id (Integer/parseInt limit))))
  
  ;; Binance endpoints
  (GET "/binance/price/:symbol" [symbol]
    (response/response (get-binance-price symbol)))
  
  ;; Twilio endpoints
  (GET "/twilio/alerts" []
    (response/response (get-twilio-alerts 50)))
  
  (GET "/twilio/alerts/:limit" [limit]
    (response/response (get-twilio-alerts (Integer/parseInt limit))))
  
  ;; System status
  (GET "/system/status" []
    (response/response (get-system-status)))
  
  ;; Catch-all
  (route/not-found (response/response {:error "Not found"} 404)))

;; Main app with middleware
(def app
  (-> api-routes
      (json/wrap-json-response)
      (json/wrap-json-body {:keywords? true})
      (cors/wrap-cors :access-control-allow-origin [#"http://localhost:8000" #"http://localhost:3000"]
                      :access-control-allow-methods [:get :post :put :delete :options]
                      :access-control-allow-headers ["Content-Type" "Authorization"])))

;; Server state
(defstate server
  :start (do
           (info "Starting Clojure HTTP API server on port 8080")
           (jetty/run-jetty app {:port 8080 :join? false}))
  :stop (do
          (info "Stopping Clojure HTTP API server")
          (.stop server)))

;; Helper function to start the API server
(defn start-api-server! []
  "Start the HTTP API server"
  (mount/start #'server))

;; Helper function to stop the API server
(defn stop-api-server! []
  "Stop the HTTP API server"
  (mount/stop #'server))
