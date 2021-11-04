# Quick benchmark forecasts for 
library(dplyr)
library(tidyr)
library(tidyverse)
library(tsibble)
library(urca)
library(feasts)
library(fable)
library(MMWRweek)

# Constants
WDIR = "~/Documents/Local_Repos/dsf-ts-forecasting"
DATA_PATH = "~/Documents/Local_Repos/dsf-ts-forecasting/DATA/ILINet.csv"
HORIZON = 3

# Set working directory
if (getwd() != WDIR){
  setwd(WDIR)
}

# Data load and processing
data <- read_csv(DATA_PATH, na="X") %>%
  mutate(week_date= MMWRweek2Date(YEAR, WEEK)) %>%
  filter(week_date >= MMWRweek2Date(2014, 1)) %>%
  filter(week_date < MMWRweek2Date(2020, 1)) %>%
  select(REGION, week_date, ILITOTAL) %>% 
  filter(!REGION %in% c("Florida", "Commonwealth of the Northern Mariana Islands")) %>%
  as_tsibble(index=week_date, key=REGION, regular=TRUE) %>%
  mutate(week_date=yearweek(week_date)) 

# CV - not exactly the same as with the python CV experiments
cv_data <- stretch_tsibble(data, .step = 7, .init = 5*52)
# make the forecasts
forecasts <- cv_data %>% 
  model(
    naive = NAIVE(ILITOTAL),
    seasonal_naive = SNAIVE(ILITOTAL),
    ets = ETS(ILITOTAL),
    ) %>% 
  forecast(h=3)

# create the granular accuracy report
accuracy_table <- 
  forecasts %>%
  accuracy(data)

# view accuracy report
accuracy_summary <- accuracy_table %>% 
  group_by(.model, .type) %>%
  summarise(
    mean_mape=mean(MAPE), 
    mean_rmse = mean(RMSE), 
    mean_mase = mean(MASE), 
    mean_rmsse=mean(RMSSE),
    )

view(accuracy_summary)

# PDF report for analysts and stakeholders
# Create a df of unique TS identifiers to evaluate plots
TS_unique <- cv_data %>% as_tibble() %>% select(REGION, .id) %>% unique()
# Generate a pdf of all the plots
PDFPath = "R_example/region_forecasts_R.pdf"
pdf(file=PDFPath, onefile = TRUE) 
# choose which models you want to see in the plot
PLOT_MODELS <- c("ets", "naive", "seasonal_naive")
for(i in 1:nrow(TS_unique)){
  par(mfrow = c(3,2))
  PLOT_REGION <- TS_unique$REGION[i]
  PLOT_ID <- TS_unique$.id[i]
  # Plotting
  plot <- forecasts %>% filter(
    REGION == PLOT_REGION &
    .id ==PLOT_ID &
    .model %in% PLOT_MODELS
    ) %>% 
    autoplot(cv_data %>% filter(week_date >= MMWRweek2Date(2018, 1)), level=NULL) + labs(title = sprintf("%s %s", PLOT_REGION, PLOT_ID))
  print(plot)
}
dev.off() 
