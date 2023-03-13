package service

import (
	"errors"
	"fmt"
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
		SetQueryParam("days", "5").
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
