package service

import (
	"errors"
	"fmt"
	"strings"
	"time"

	"weather/app/models"

	"github.com/go-resty/resty/v2"
)

type Service struct {
	rest       *resty.Client
	weatherUrl string
	weatherKey string
}

func NewService(weatherUrl, weatherKey string) *Service {
	return &Service{
		weatherUrl: weatherUrl,
		weatherKey: weatherKey,
		rest:       resty.New().SetTimeout(time.Minute),
	}
}

func (s *Service) GetForecast(location string) (*models.GetForecastResponse, error) {
	url := fmt.Sprintf("%s/forecast.json", s.weatherUrl)

	resp, err := s.rest.R().
		SetResult(&models.GetForecastResponse{}).
		SetError(&models.ErrorResponse{}).
		SetQueryParam("key", s.weatherKey).
		SetQueryParam("q", location).
		SetQueryParam("days", "2").
		Get(url)

	err = handleError(resp, err)
	if err != nil {
		return nil, err
	}

	res, ok := resp.Result().(*models.GetForecastResponse)
	if !ok {
		return nil, fmt.Errorf("failed to cast result response")
	}

	return res, nil
}

func (s *Service) ParseData(data *models.GetForecastResponse, index string) []string {
	if data == nil {
		panic(fmt.Errorf("empty data"))
	}

	day := s.ParseDay(data.Forecast.Forecastday[0], index)
	hours, counter := s.ParseHours(data.Forecast.Forecastday[0])
	var res []string
	for _, hour := range hours {
		res = append(res, day+hour)
	}
	if counter < 12 {
		//parse next day
		day = s.ParseDay(data.Forecast.Forecastday[1], index)
		hours, _ = s.ParseHours(data.Forecast.Forecastday[1])
		for _, hour := range hours {
			if counter == 12 {
				break
			}
			counter++
			res = append(res, day+hour)
		}
	}

	return res
}

func (s *Service) ParseDay(data models.Forecastday, index string) string {
	var res strings.Builder

	res.WriteString(index)
	res.WriteString(",")
	tt, err := time.Parse(time.RFC3339, data.Date+"T15:04:05Z")
	if err != nil {
		panic(err)
	}
	res.WriteString(fmt.Sprint(int(tt.Month())))
	res.WriteString("/")
	res.WriteString(fmt.Sprint(tt.Day()))
	res.WriteString("/")
	res.WriteString(fmt.Sprint(tt.Year()))
	res.WriteString(",")

	var tempmax float64 = -999999
	var tempmin float64 = 999999
	var tempSum float64 = 0
	var dewSum float64 = 0

	for _, hour := range data.Hour {
		if hour.FeelslikeC > tempmax {
			tempmax = hour.FeelslikeC
		}

		if hour.FeelslikeC < tempmin {
			tempmin = hour.FeelslikeC
		}

		tempSum += hour.FeelslikeC
		dewSum += hour.DewpointC
	}
	res.WriteString(fmt.Sprint(data.Day.MaxtempC))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(data.Day.MintempC))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(data.Day.AvgtempC))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(tempmax))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(tempmin))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(float64(int(tempSum*100/24)) / 100))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(float64(int(dewSum*100/24)) / 100))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(data.Day.Avghumidity))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(data.Day.TotalprecipMm))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(data.Day.AvgvisKm))
	res.WriteString(",")
	res.WriteString(fmt.Sprint(data.Day.Uv))
	res.WriteString(",")
	sunrise := strings.Split(data.Astro.Sunrise, " ")
	sunset := strings.Split(data.Astro.Sunset, " ")
	tt, err = time.Parse(time.RFC3339, data.Date+"T"+sunrise[0]+":05Z")
	if err != nil {
		panic(err)
	}

	res.WriteString(fmt.Sprint(tt.Add(time.Hour * 2).Unix()))
	res.WriteString(",")

	tt, err = time.Parse(time.RFC3339, data.Date+"T"+sunset[0]+":05Z")
	if err != nil {
		panic(err)
	}
	res.WriteString(fmt.Sprint(tt.Add(time.Hour * 14).Unix()))
	res.WriteString(",")

	res.WriteString(fmt.Sprint(moonPhase(data.Astro.MoonPhase)))
	res.WriteString(",")

	res.WriteString(data.Day.Condition.Text)
	res.WriteString(",")

	return res.String()
}

func (s *Service) ParseHours(data models.Forecastday) ([]string, int) {
	now := time.Now()
	counter := 0
	var result []string
	for _, hour := range data.Hour {
		timeTemp := strings.Split(hour.Time, " ")
		tt, err := time.Parse(time.RFC3339, data.Date+"T"+timeTemp[1]+":00+"+strings.Split(now.Format(time.RFC3339), "+")[1])
		if err != nil {
			panic(err)
		}
		if now.After(tt) {
			continue
		}
		var res strings.Builder

		res.WriteString(timeTemp[1] + ":00")
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.TempC))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.FeelslikeC))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.Humidity))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.DewpointC))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.PrecipIn))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.GustKph))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.WindKph))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.WindDegree))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.PressureMb))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.VisKm))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.Cloud))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.Uv))
		res.WriteString(",")
		res.WriteString(fmt.Sprint(hour.Condition.Text))
		result = append(result, res.String())
		counter++
	}

	return result, counter
}

func moonPhase(moon string) float64 {
	switch moon {
	case "New Moon":
		return 0
	case "Waxing Crescent":
		return 0.25
	case "First Quarter":
		return 0.5
	case "Waxing Gibbous":
		return 0.75
	case "Full Moon":
		return 1
	case "Waning Gibbous":
		return 0.75
	case "Last Quarter":
		return 0.5
	case "Waning Crescent":
		return 0.25
	}

	panic(fmt.Errorf("unknown moon phase"))
}

func handleError(resp *resty.Response, err error) error {
	if err != nil {
		return err
	}

	if resp.IsError() {
		body, ok := resp.Error().(*models.ErrorResponse)
		if !ok {
			return fmt.Errorf("failed to cast error response")
		}

		return errors.New(body.Error.Message)
	}

	return nil
}
