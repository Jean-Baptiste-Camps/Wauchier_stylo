# sudo apt-get install r-cran-haven r-cran-car r-cran-rmpi
# For car to install : sudo apt-get install gfortran liblapack-dev liblapack3 libopenblas-base libopenblas-dev libcurl4-openssl-dev
#
#
#

pkgLoad <- function( packages = "favourites" ) {
  
  if( length( packages ) == 1L && packages == "favourites" ) {
    packages <- c("stylo", "dendextend", "kohonen", "FactoMineR", "factoextra", "NMF"
    )
  }
  
  packagecheck <- match( packages, utils::installed.packages()[,1] )
  
  packagestoinstall <- packages[ is.na( packagecheck ) ]
  
  if( length( packagestoinstall ) > 0L ) {
    utils::install.packages(packagestoinstall, dependencies=TRUE)
  } else {
    print( "All requested packages already installed" )
  }
  
  for( package in packages ) {
    suppressPackageStartupMessages(
      library( package, character.only = TRUE, quietly = TRUE )
    )
  }
  
}
pkgLoad()



# 1.12.6 and 1.12.4 would not install
#install.packages("https://github.com/Rdatatable/data.table/archive/1.12.2.tar.gz", repos=NULL, type="source")
#install.packages("https://github.com/kassambara/ggpubr/archive/v0.2.3.tar.gz", repos=NULL, type="source")
#install.packages("https://github.com/wilkelab/cowplot/archive/1.0.0.tar.gz", repos=NULL, type="source")
#install.packages("rio")