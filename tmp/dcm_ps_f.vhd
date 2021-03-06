--------------------------------------------------------------------------------
-- COPYRIGHT(C) 2006 by @@@@@@@@@@@@ ALL RIGHTS RESERVED
--------------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;

-- pragma translate_off
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
-- pragma translate_on

entity dcm_ps_f is
  generic(
    PS  : integer
  );
  port(
    RST          : in  std_logic;              -- リセット
    CLK_IN        : in  std_logic;             -- クロック入力
    CLK_FB_IN      : in  std_logic;            -- クロックFB入力
    CLK_OUT        : out  std_logic            -- クロック出力
  );
end dcm_ps_f;

--------------------------------------------------
-- Architecture Body Define
--------------------------------------------------
architecture rtl of dcm_ps_f is

--------------------------------------------------
-- Components
--------------------------------------------------

component BUFG 
  port (
    I          : in  std_logic;
    O          : out  std_logic
  ); 
end component;
--
component DCM
-- pragma translate_off
  generic ( 
       DLL_FREQUENCY_MODE : string := "LOW";
       DUTY_CYCLE_CORRECTION : boolean := TRUE;
       CLKOUT_PHASE_SHIFT : string := "VARIABLE";
       PHASE_SHIFT  : integer := 0;
       STARTUP_WAIT : boolean := FALSE
      );  
-- pragma translate_on
  port (CLKIN   : in  std_logic;
       CLKFB    : in  std_logic;
       DSSEN    : in  std_logic;
       PSINCDEC : in  std_logic;
       PSEN     : in  std_logic;
       PSCLK    : in  std_logic;
       RST      : in  std_logic;
       CLK0     : out std_logic;
       CLK90    : out std_logic;
       CLK180   : out std_logic;
       CLK270   : out std_logic;
       CLK2X    : out std_logic;
       CLK2X180 : out std_logic;
       CLKDV    : out std_logic;
       CLKFX    : out std_logic;
       CLKFX180 : out std_logic;
       LOCKED   : out std_logic;
       PSDONE   : out std_logic;
       STATUS   : out std_logic_vector(7 downto 0)
      );
end component;
--
-- Attributes

attribute DLL_FREQUENCY_MODE : string; 
attribute DUTY_CYCLE_CORRECTION : string;
attribute CLKOUT_PHASE_SHIFT : string;
attribute PHASE_SHIFT  : integer; 
attribute STARTUP_WAIT : string; 

attribute DLL_FREQUENCY_MODE of U_DCM: label is "LOW";
attribute DUTY_CYCLE_CORRECTION of U_DCM: label is "TRUE";
attribute CLKOUT_PHASE_SHIFT of U_DCM: label is "FIXED";
attribute PHASE_SHIFT  of U_DCM: label is 192;
attribute STARTUP_WAIT of U_DCM: label is "FALSE";

--------------------------------------------------
-- Signals
--------------------------------------------------
signal  logic_0        : std_logic;      -- 0固定信号
signal  CLK0_OUT      : std_logic;       -- DCM出力クロック

begin

-- *********************************************************************
-- 固定信号
-- *********************************************************************
  logic_0 <= '0';                   -- 0固定信号


U_DCM : DCM 
-- pragma translate_off
  generic map(
    CLKOUT_PHASE_SHIFT  => "FIXED",
    PHASE_SHIFT         => PS       -- n/256*Tns shift For SIM
--  PHASE_SHIFT         => 192      -- n/256*Tns shift For SIM
  )
-- pragma translate_on
  port map(
    RST          => RST        ,    -- リセット
    CLKIN        => CLK_IN     ,    -- PHASE SHIFT入力クロック
    CLKFB        => CLK_FB_IN  ,    -- FB入力
    DSSEN        => logic_0    ,    
    PSINCDEC     => logic_0    ,    -- 位相シフトの増分/減分
    PSEN         => logic_0    ,    -- 位相シフトイネーブル
    PSCLK        => logic_0    ,    -- 位相シフトクロック
    CLK0         => CLK0_OUT        -- PHASE SHIFT出力クロック
--    CLK90      => CLK90      ,    --
--    CLK180     => CLK180     ,    --
--    CLK270     => CLK270     ,    --
--    CLK2X      => CLK2X      ,    --
--    CLK2X180   => CLK2X180   ,    --
--    CLKDV      => CLKDV      ,    --
--    CLKFX      => CLKFX      ,    --
--    CLKFX180   => CLKFX180   ,    --
--    LOCKED     => LOCKED     ,    --
--    PSDONE     => PSDONE     ,    --
--    STATUS     => STATUS     ,    --
  );

U_BUFG : BUFG
  port map(
    I  => CLK0_OUT,                 -- DCM出力クロック
    O  => CLK_OUT                   -- DCM出力クロック(BUFG後)
  );

end rtl;
