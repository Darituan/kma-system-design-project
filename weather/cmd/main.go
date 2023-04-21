package main

import (
	"net/http"
	"os"
	validator "weather/app/api"
	"weather/app/service"
	"weather/app/types"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		panic(err)
	}

	port := os.Getenv("PORT")
	weatherUrl := os.Getenv("WEATHER_API_URL")
	weatherKey := os.Getenv("WEATHER_API_KEY")

	service := service.NewService(weatherUrl, weatherKey)

	r := gin.Default()
	r.GET("/:location", func(ctx *gin.Context) {
		location := ctx.Param("location")

		location, err := validator.ValidateLocation(location)
		if err != nil {
			ctx.JSON(http.StatusBadRequest, gin.H{
				"error": err.Error(),
			})
			return
		}

		data, err := service.GetForecast(location)
		if err != nil {
			ctx.JSON(http.StatusBadRequest, gin.H{
				"error": err.Error(),
			})
			return
		}

		ctx.JSON(http.StatusOK, gin.H{
			"data": data,
		})
	})

	r.GET("/forecast", func(ctx *gin.Context) {
		var res []string
		for location, index := range types.GetLocationForecast() {
			data, err := service.GetForecast(location)
			if err != nil {
				ctx.JSON(http.StatusBadRequest, gin.H{
					"error": err.Error(),
				})
				return
			}

			res = append(res, service.ParseData(data, index)...)
		}
		ctx.JSON(http.StatusOK, gin.H{
			"data": res,
		})
	})

	if err := r.Run(":" + port); err != nil {
		panic(err)
	}
}
