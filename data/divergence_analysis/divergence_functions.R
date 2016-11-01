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