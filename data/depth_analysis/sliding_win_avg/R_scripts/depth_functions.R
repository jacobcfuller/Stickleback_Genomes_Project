######################################################################################
#                             Make tables of read data                               #      
######################################################################################

#pulls depth_txt files into table
load_depth_to_table<-function(dir,chr){
  files<-list.files(dir,full.names = TRUE)
  table<-read.table(file=files[1],header=TRUE)
  for (f in files){
    if (f != files[1]){
      table <- cbind(table,read.table(file=f,header=TRUE))
    }
  }
  bp_pos=get_bp_pos_vector(table,chr)
  table <- cbind(bp_pos,table)
  return(table)
}

#gets the # of average reads (i.e., chr length/sliding win. interval size)
#default sliding win. interval is 500
get_avg_count_vec<-function(table){
  len=length(table[[1]])
  avg_vec=seq(1:len)
  return(avg_vec)
}

#create vector of bp_pos for each avg read
get_bp_pos_vector<-function(table,chr){
  if (chr=="XIX"){
    chr_size=20612724
  }
  if(chr=="IX"){
    chr_size=20593793
  }
  if(chr=="XXI"){
    chr_size=17357772
  }
  avg_vec=get_avg_count_vec(table)
  bp_pos_vec=avg_vec*(chr_size/length(avg_vec))
  
}

#load to table and compensate read count
load_to_table_to_test<-function(male,female,male_RC,female_RC){
  POF<-read.table(female,header=TRUE)
  male10<-read.table(male,header=TRUE)
if(male_RC>female_RC){
    POF<-read_count_comp(male_RC,female_RC,POF)
  } else if(male_RC<female_RC){
    male10<-read_count_comp(female_RC,male_RC,male10)
  }
  bp_pos<-get_bp_pos_vector(male10,"XIX")
  logMale10POF <- log2(male10/POF)
  log_graph<-cbind(bp_pos,logMale10POF)
  colnames(log_graph)<-c("bp_pos","log(male/female)")
  #remove NaN
  log_graph<-na.exclude(log_graph)
  #remove Inf/-Inf
  log_graph<-log_graph[is.finite(rowSums(log_graph)),]
  return(log_graph)
}


#####################################################################################
#                                   Analysis                                        #
#####################################################################################


#really slow
second_deriv<-function(table,col){
  line<-loess(col ~ bp_pos,table)
  deriv_2<-(diff(diff(line$fitted)))
  return(data.frame(deriv_2))
}

ruff_plot<-function(table,bp_pos,y_axis){
  library(ggplot2)
  `log(male/female)`= y_axis
  ggplot(table,aes(x=bp_pos,y=`log(male/female)`))+geom_point(size=0.3,alpha=0.5)+geom_smooth()+coord_cartesian(ylim = c(-5,5))
}

ruff_plot_limit<-function(table,bp_pos,y_axis){
  library(ggplot2) 
  ggplot(table,aes(x=bp_pos,y=y_axis))+geom_point(size=0.3,alpha=0.5)+geom_smooth()+scale_y_continuous(limits=c(-5,5))
}

read_count_comp<-function(big_count,small_count,small_samp){
  ratio = (big_count/small_count)
  small_samp <- ratio*(small_samp)
  return(small_samp)
}