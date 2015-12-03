isEmpty(phenoVein_General_PRI_INCLUDED) {
  message ( loading phenoVein_General.pri )
}
# **InsertLicense** code
# -----------------------------------------------------------------------------
# phenoVein_General prifile
#
# \file    phenoVein_General.pri
# \author  Jonas Bühler
# \date    2015-03-13
#
# Contains all phenoVein modules
#
# -----------------------------------------------------------------------------

# include guard against multiple inclusion
isEmpty(phenoVein_General_PRI_INCLUDED) {

phenoVein_General_PRI_INCLUDED = 1

# -- System -------------------------------------------------------------

include( $(MLAB_MeVis_Foundation)/Configuration/SystemInit.pri )

# -- Define local PACKAGE variables -------------------------------------

PACKAGE_ROOT    = $$(MLAB_phenoVein_General)
PACKAGE_SOURCES = "$$(MLAB_phenoVein_General)"/Sources

# Add package library path
LIBS          += -L"$${PACKAGE_ROOT}"/lib

# -- Projects -------------------------------------------------------------

# NOTE: Add projects below to make them available to other projects via the CONFIG mechanism

# You can use this example template for typical projects:
#MLMyProject {
#  CONFIG_FOUND += MLMyProject
#  INCLUDEPATH += $${PACKAGE_SOURCES}/ML/MLMyProject
#  win32:LIBS += MLMyProject$${d}.lib
#  unix:LIBS += -lMLMyProject$${d}
#}

# -- ML Projects -------------------------------------------------------------

# -- Inventor Projects -------------------------------------------------------

# -- Shared Projects ---------------------------------------------------------

# End of projects ------------------------------------------------------------

}