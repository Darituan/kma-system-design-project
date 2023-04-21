package types

var locations = map[string]string{
	"Kyiw":            "Kiev",
	"Cherkasy":        "Cherkasy",
	"Chernihiv":       "Chernihiv",
	"Chernivtsi":      "Chernivtsi",
	"Dnipro":          "Dnipropetrovsk",
	"Donetsk":         "Donetsk,Ukraine",
	"Ivano-Frankivsk": "Ivano-Frankivsk,Ukraine",
	"Kharkiv":         "Kharkiv",
	"Kherson":         "Kherson",
	"Khmelnytskyi":    "49.25,27.00",
	"Kropyvnytskyi":   "Kirovohrad",
	"Luhansk":         "Luhansk",
	"Lviv":            "Lviv",
	"Mykolaiv":        "46.5830,31.5942",
	"Odesa":           "Odesa",
	"Poltava":         "Poltava",
	"Rivne":           "Rivne",
	"Sumy":            "Sumy",
	"Ternopil":        "Ternopil",
	"Vinnytsia":       "Vinnytsya",
	"Lutsk":           "Lutsk,Ukraine",
	"Uzhhorod":        "Uzhhorod",
	"Zaporizhzhia":    "47.51,35.0703",
	"Zhytomyr":        "Zhytomyr",
}

var locationsForecast = map[string]string{
	"Kiev":                    "10",
	"Cherkasy":                "23",
	"Chernihiv":               "25",
	"Chernivtsi":              "24",
	"Dnipropetrovsk":          "4",
	"Donetsk,Ukraine":         "5",
	"Ivano-Frankivsk,Ukraine": "9",
	"Kharkiv":                 "20",
	"Kherson":                 "21",
	"49.25,27.00":             "22",
	"Kirovohrad":              "11",
	"Luhansk":                 "12",
	"Lviv":                    "13",
	"46.5830,31.5942":         "14",
	"Odesa":                   "15",
	"Poltava":                 "16",
	"Rivne":                   "17",
	"Sumy":                    "18",
	"Ternopil":                "19",
	"Vinnytsya":               "2",
	"Lutsk,Ukraine":           "3",
	"Uzhhorod":                "7",
	"47.51,35.0703":           "8",
	"Zhytomyr":                "6",
}

func GetLocation(location string) (string, bool) {
	res, ok := locations[location]

	return res, ok
}

func GetLocationForecast() map[string]string {
	return locationsForecast
}
