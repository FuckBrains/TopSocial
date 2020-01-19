package datehandler

import (
	"time"
	"app/shared/localize"
	"fmt"

	"strconv"
)

func TimeAgo(epochDate float64) string{

	nowEpoch := time.Now().Unix()
	differenceInMinutes := (float64(nowEpoch) - epochDate)/60
	//return strconv.FormatFloat(differenceInMinutes,'f',5,64)
	//return strconv.FormatFloat(float64(nowEpoch),'f',5,64) + strconv.FormatFloat(epochDate,'f',5,64)
	if (differenceInMinutes < 1) {
		return localize.GetInstance().TranslateFunc("reldate_justnow")
	}
	if (differenceInMinutes <= 1) {
		return localize.GetInstance().TranslateFunc("reldate_lessthanminute")
	}
	if (differenceInMinutes < 2)		{
		return localize.GetInstance().TranslateFunc("reldate_oneminute")
	}
	if (differenceInMinutes < 60) 		{
		minutes:=strconv.FormatFloat(differenceInMinutes,'f',0,64)
		return localize.GetInstance().TranslateFunc("reldate_minutesago",minutes)
	}
	if (differenceInMinutes < 120)		{
		return localize.GetInstance().TranslateFunc("reldate_onehour")
	}
	if (differenceInMinutes < 24*60) 	{
		xx:=float64(differenceInMinutes)/float64(60)
		hours:=strconv.FormatFloat(xx,'f',0,64)
		return localize.GetInstance().TranslateFunc("reldate_hoursago",hours)
	}
	if (differenceInMinutes < 2*24*60)	{
		return localize.GetInstance().TranslateFunc("reldate_yesterday")
	}
	if (differenceInMinutes < 7*24*60) 	{
		xx:=float64(differenceInMinutes)/float64((60*24))
		days:= strconv.FormatFloat(xx,'f',0,64)
		return localize.GetInstance().TranslateFunc("reldate_daysago",days)
	}
	if (differenceInMinutes < 14*24*60)	{
		return localize.GetInstance().TranslateFunc("reldate_lastweek")
	}
	if (differenceInMinutes < 21*24*60) 	{
		return localize.GetInstance().TranslateFunc("reldate_twoweeksago")
	}
	if (differenceInMinutes < 28*24*60) 	{
		return localize.GetInstance().TranslateFunc("reldate_threeweeksago")
	}
	if (differenceInMinutes < 30*24*60) 	{
		return localize.GetInstance().TranslateFunc("reldate_lastmonth")
	}
	if (differenceInMinutes < 365*24*60) 	{
		xx:=float64(differenceInMinutes)/float64((30*24*60))
		months:= strconv.FormatFloat(xx,'f',0,64)
		return localize.GetInstance().TranslateFunc("reldate_monthsago",months)
	}
	if (differenceInMinutes < 730*24*60)	{
		return localize.GetInstance().TranslateFunc("reldate_lastyear")
	}
	years,_:=fmt.Printf("%.0f", float64(differenceInMinutes)/float64((365*24*60)))
	return localize.GetInstance().TranslateFunc("reldate_yearsago",years)

}

//func ToSolar(date time.Time) string{
//
//}
//
//
//func ToGregorian(solarDate string) time.Time{
//
//}