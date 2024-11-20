# lbc-monitor-bias
Scripts to monitor LBC bias and readnoise

LBC_Bias_Statistics.py: 

 Inputs are (1) a list of bias images; and 
            (2) a region for statistics for the bias and readnoise in the format [x1,x2,y1,y2], where the 
             x-axis runs from the first to last column and the y-axis runs from the first to last row. 
             Statistics on the overscan are hardwired to use all of the rows but skip the first 50 columns.

 Outputs 4 files, one for each chip.

 Example:
LBC_Bias_Statistics.py <bias.list> [601,1600,2501,3500]
 
plotbias.py: 

 Creates a 2-panel plot with bias vs time (top) and readnoise vs time (bottom). It requires the 4 files 
output by LBC_Bias_Statistics.py and a file of dates which is the output of getheadlist <bias.list> date-obs
(A future version could just convert the Julian dates in the output files to YYYY-MM-DD time strings).

 Example: 
plotbias.py <outfile_chip1> <outfile_chip2> <outfile_chip3> <outfile_chip4> <outfile_dates>

