-- LOCAL READ CONTROLLER ( ifpga <- pfpga )
-- (LOCAL_READ_IFに開始信号を全チップ回数分送るモジュール)
-- by Tsuyoshi Hamada 2005/01/04
-- メモ : 
--   NQWORDとってくるのに必要なLOCAL_READ_IFのクロック(BUSY) : NQWORD + 8(レイテンシ:INTF_LAT) クロック
-- 
-- (0) IFに START_AD, NQWORD をセット     : 1クロック
-- (1) IFに CHIPSEL, MEM_AD_BASE をセット : 1クロック
-- (2) IFの EXEC を上げる                 : 1クロック
-- (3) IFに EXEC を下げる                 : 1クロック
-- (4) IFが転送を終了するまで待つ         : I_NC クロック(I_NC= NPIPE*pow(2,NBIT_L_ADRO)
-- (5) (1)から(4)までを4チップ分繰り返す.
--
-- (※) LOCAL_READ_IFの転送に必要なクロックは決まっているので転送終了フラグは見ない.
-- (※) l_adroのビット幅(NBIT_L_ADRO)を変えた場合はpromを焼きなおす必要があることに注意.(直すのは上のモジュール)

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;

entity LOCAL_READ_CNT is
  generic (
           CNT_WIDTH     : integer := 16;      -- program counter bit-width
           FO_BASE       : integer := 24576;   -- = 0x6000
           NBIT_L_ADRO   : integer := 3;       -- Bit-Length of l_ado(pgpg_mem.vhd)
           INTF_LAT      : integer := 8        -- LOCAL_READ_IF latency (clock)
  );
  port (
    -- from LOCAL_READ
    NPIPE : in std_logic_vector(7 downto 0);     -- number of pipelines per chip
    -- from LOCAL_READ_DONE
    CALC_DONE  : in std_logic;   -- pulse
    -- to LOCAL_READ_DONE
    FETCH_DONE : out std_logic;  -- pulse

    -- to LOCAL_READ_IF
    EXEC     : out std_logic;                     -- pulse
    START_AD : out std_logic_vector(18 downto 0); -- 19 bit
    NQWORD   : out std_logic_vector( 8 downto 0); --  9 bit
    CHIPSEL  : out std_logic_vector( 3 downto 0); --  4 bit
    MEM_AD_BASE : out std_logic_vector(12 downto 0);
    -- from LOCAL_READ_IF
--    BUSY_IF : in std_logic;
 
    RST : in  std_logic;
    CLK : in  std_logic
    );
end LOCAL_READ_CNT;

architecture rtl of LOCAL_READ_CNT is

signal hit0,hit1 : std_logic :='0';
signal cnt,cntr : std_logic_vector(CNT_WIDTH-1 downto 0) :=(others=>'0');
signal cnt_en : std_logic :='0';
signal is_finish,is_finishr : std_logic :='0';

----
signal c_start_ad   : std_logic_vector(18 downto 0) :=(others=>'0');
signal c_nqword     : std_logic_vector(18 downto 0) :=(others=>'0');
signal c_chipsel    : std_logic_vector(18 downto 0) :=(others=>'0');
signal c_mem_offset : std_logic_vector(18 downto 0) :=(others=>'0');
begin

  FETCH_DONE <= is_finish; -- transfer done pulse

  hit0 <= CALC_DONE;
  process (CLK) begin
    if (CLK'event and CLK='1') then
      is_finishr <= is_finish;
      hit1 <= hit0;
    end if;
  end process;

  -- PROGRAM COUNTER
  cntr <= cnt + conv_std_logic_vector(1, CNT_WIDTH);
  process (RST,CLK,hit0,hit1,cnt_en) begin
    if (RST = '1') then
      cnt <= (others=>'0');
    elsif (CLK'event and CLK='1') then
      if((hit0 = '1') AND (hit1 = '0')) then
        cnt <= (others=>'0');
      elsif(cnt_en = '1') then
        cnt <= cntr;
      end if;
    end if;
  end process;

  -- COUNTER ENABLE (counting up signal)
  process (RST,CLK,hit0,hit1,is_finish,is_finishr) begin
    if (RST = '1') then
      cnt_en <= '0';
    elsif (CLK'event and CLK='1') then
      if((hit0 = '1') AND (hit1 = '0')) then
        cnt_en <= '1';
      elsif((is_finish = '1') AND (is_finishr = '0')) then
        cnt_en <= '0';
      end if;
    end if;
  end process;

  ------------------------------------------------------------- PROGRAM
  process (RST,CLK,cnt)
      variable I_NPIPE : integer;
      variable I_NFI   : integer;
      variable I_NC    : integer;
      variable I_MAB   : integer;
      variable I_NQW   : integer;
  begin
    if (RST='1') then
      is_finish <= '0';
    elsif (CLK'event and CLK='1') then

      --= = = = = = = = = = = = = = = = = = = = INTEGER VARLUES
      I_NPIPE := conv_integer(NPIPE);
      I_NFI   := (2**NBIT_L_ADRO);
--      I_NFI   := (2**2);  -- トップからのジェネリックの伝播がうまくいきませんので注意
      I_NC    := I_NPIPE*I_NFI + INTF_LAT;
      I_MAB   := I_NPIPE*I_NFI;
      I_NQW   := I_NPIPE*I_NFI - 1;
      --= = = = = = = = = = = = = = = = = = = = = = = = = = = =

      if(    cnt = conv_std_logic_vector(0, CNT_WIDTH) ) then
        is_finish <= '0';
        NQWORD   <= conv_std_logic_vector(I_NQW, 9);
        START_AD <= conv_std_logic_vector(FO_BASE, 19);
      -- ================================================================================ CHIP 0
      elsif( cnt = conv_std_logic_vector(1, CNT_WIDTH) ) then
        MEM_AD_BASE <= conv_std_logic_vector(0, 13);
        CHIPSEL  <= "0001";
      elsif( cnt = conv_std_logic_vector(2, CNT_WIDTH) ) then
        EXEC <= '1';
      elsif( cnt = conv_std_logic_vector(3, CNT_WIDTH) ) then
        EXEC <= '0';
      -- ================================================================================ CHIP 1
      elsif( cnt = conv_std_logic_vector(3 + 1*I_NC, CNT_WIDTH) ) then
        MEM_AD_BASE <= conv_std_logic_vector(1*I_MAB  , 13);
        CHIPSEL  <= "0010";
      elsif( cnt = conv_std_logic_vector(4 + 1*I_NC, CNT_WIDTH) ) then
        EXEC <= '1';
      elsif( cnt = conv_std_logic_vector(5 + 1*I_NC, CNT_WIDTH) ) then
        EXEC <= '0';
      -- ================================================================================ CHIP 2
      elsif( cnt = conv_std_logic_vector(5 + 2*I_NC, CNT_WIDTH) ) then
        MEM_AD_BASE <= conv_std_logic_vector(2*I_MAB, 13);
        CHIPSEL  <= "0100";
      elsif( cnt = conv_std_logic_vector(6 + 2*I_NC, CNT_WIDTH) ) then
        EXEC <= '1';
      elsif( cnt = conv_std_logic_vector(7 + 2*I_NC, CNT_WIDTH) ) then
        EXEC <= '0';
      -- ================================================================================ CHIP 3
      elsif( cnt = conv_std_logic_vector(7 + 3*I_NC, CNT_WIDTH) ) then
        MEM_AD_BASE <= conv_std_logic_vector(3*I_MAB, 13);
        CHIPSEL  <= "1000";
      elsif( cnt = conv_std_logic_vector(8 + 3*I_NC, CNT_WIDTH) ) then
        EXEC <= '1';
      elsif( cnt = conv_std_logic_vector(9 + 3*I_NC, CNT_WIDTH) ) then
        EXEC <= '0';
      -- ================================================================================ FINISH
      elsif( cnt = conv_std_logic_vector(9 + 4*I_NC, CNT_WIDTH) ) then
        is_finish <= '1';
      elsif( cnt = conv_std_logic_vector(10 + 4*I_NC, CNT_WIDTH) ) then
        is_finish <= '0';
      else
      end if;

    end if;
  end process;

end rtl;

