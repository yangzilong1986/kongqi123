from sqlalchemy import Column, Date, DateTime, Integer, String, Text, Float, text


class HistoryCity(Base):
    __tablename__ = 'history_city'

    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(30), server_default=text("''::character varying"))
    city_url = Column(String(1024), server_default=text("''::character varying"))


class HistoryMonth(Base):
    __tablename__ = 'history_month'

    hm_id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    city_name = Column(String(30), server_default=text("''::character varying"))
    hm_year = Column(Integer)
    hm_month = Column(Integer)
    hm_aqi = Column(Integer)
    hm_aqi_min = Column(Integer)
    hm_aqi_max = Column(Integer)
    hm_quality = Column(String(30), server_default=text("''::character varying"))
    hm_pm25 = Column(Float)
    hm_pm10 = Column(Float)
    hm_so2 = Column(Float)
    hm_co = Column(Float)
    hm_no2 = Column(Float)
    hm_o3 = Column(Float)
    hm_rank = Column(Integer)
    hm_day_url = Column(String(255), server_default=text("''::character varying"))


class HistoryDay(Base):
    __tablename__ = 'history_day'

    hd_id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    city_name = Column(String(30), server_default=text("''::character varying"))
    hd_date = Column(Date)
    hd_aqi = Column(Integer)
    hd_aqi_min = Column(Integer)
    hd_aqi_max = Column(Integer)
    hd_quality = Column(String(30), server_default=text("''::character varying"))
    hd_pm25 = Column(Float)
    hd_pm10 = Column(Float)
    hd_so2 = Column(Float)
    hd_co = Column(Float)
    hd_no2 = Column(Float)
    hd_o3 = Column(Float)
    hd_rank = Column(Integer)

