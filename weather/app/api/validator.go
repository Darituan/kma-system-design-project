package validator

import (
	"errors"
	"weather/app/types"
)

func ValidateLocation(location string) (string, error) {
	res, ok := types.GetLocation(location)

	if !ok {
		return "", errors.New("location bad")
	}

	return res, nil
}
