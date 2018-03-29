use warnings;
use Time::HiRes qw/time/;

my $start=time;

open(FD, "c:/yunshang_10m_line.log") || die("can not open file");
my $num = 0;
my $total = 0;
while(<FD>){
  $total++;
  if(m/cur_wnd.*(20|21|31)/){
    $num++;
  }
}
print("find ".$num." match \n");
print("total ".$total." lines \n");
my $end = time;
print("cost ".($end-$start)." sec \n");
