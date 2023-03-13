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

func GetLocation(location string) (string, bool) {
	res, ok := locations[location]

	return res, ok
}
