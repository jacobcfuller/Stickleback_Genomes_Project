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

load_to_table_to_test<-function(male,female){
  POF<-read.table(female,header=TRUE)
  male10<-read.table(male,header=TRUE)
  bp_pos<-get_bp_pos_vector(male10,"XIX")
  logMale10POF <- log2(male10/POF)
  log_graph<-cbind(bp_pos,logMale10POF)
  colnames(log_graph)<-c("bp_pos","log(male/female)")
  return(log_graph)
}


#####################################################################################
#                                   Analysis                                        #
#####################################################################################


#kind of slow
second_deriv<-function(table,col){
  line<-loess(col ~ bp_pos, table)
  deriv_2<-(diff(diff(line$fitted)))
  return(deriv_2)
}

ruff_plot<-function(){
  library(ggplot2)
  ggplot(test_graph,aes(x=test_graph$bp_pos,y=test_graph$`log(male/female)`))+geom_point(size=0.3,alpha=0.5)+geom_smooth()
}