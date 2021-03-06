import sys
from utilities import FileHelper
import constants
import numpy

''' Algorithm imports '''
from LloydsAlgorithm.VectorialCuantification import VectorialCuantification
from BayesAlgorithm.Bayes import Bayes, Class as BayesClass

sys.path.append( "SOM-Algorithm/" )
from SOM import SOM

sys.path.append( "k-medidas/" )
from KMeans import KMeans,Class as KMeansClass
''' End of algorithm imports '''

''' This method loads KMeans needed values and adds the to the wrapper class KMeans '''

def loadFileKMeans(file,classNameIndex):
	
	k = KMeans(constants.getN())
	fileHelper = FileHelper()
	

	c1 = KMeansClass(0,"Iris-setosa")
	c1.setVCenter([4.6,3.0,4.0,0.0])
	c2 = KMeansClass(1,"Iris-versicolor")
	c2.setVCenter([6.8,3.4,4.6,0.7])

	k.addClass(c1)
	k.addClass(c2)
	try:
		f = fileHelper.openReadOnlyFile(file)
		
		lineas = f.readlines()
		uMatrix = constants.getKMeansInitializeUMAtrix(len(lineas))
		k.setUMatrix(uMatrix)
		xVector = []

		for linea in lineas:

			xVector = linea.strip("\r\n").split(",")
			del xVector[classNameIndex-1]
			xVector = [float(x) for x in xVector]

			k.addXVector(xVector)

		return k
	except:
		print("Error al leer el fichero")

''' This method loads Bayes needed values and adds the to the wrapper class Bayes '''

def loadFileBayes(file,classNameIndex):

	b = Bayes(constants.getN())
	fileHelper = FileHelper()

	try:
		f = fileHelper.openReadOnlyFile(file)
		
		lineas = f.readlines()
		xVector = []

		for linea in lineas:

			xVector = linea.strip("\r\n").split(",")
			className = xVector[classNameIndex-1]
			del xVector[classNameIndex-1]
			xVector = [float(x) for x in xVector]

			b.addX(xVector,className)

		return b
	except:
		print("Error al leer el fichero")

''' This method loads Lloyds needed values and adds the to the wrapper class VectorialCuantification '''

def loadFileLloyd(file,classNameIndex):

	toleranceLimit = constants.getLloydsTolerance()
	lloyd = VectorialCuantification(N=constants.getN(),maxK=constants.getLloydsMaxK(),tolerance=toleranceLimit)
	lloyd.setGammaK(constants.getLLoydsGammaK())
	#centers
	lloyd.addInitialCenter([4.6,3.0,4.0,0.0],"Iris-setosa")
	lloyd.addInitialCenter([6.8,3.4,4.6,0.7],"Iris-versicolor")
	fileHelper = FileHelper()

	try:
		f = fileHelper.openReadOnlyFile(file)
		
		lineas = f.readlines()
		xVector = []

		for linea in lineas:

			xVector = linea.strip("\r\n").split(",")
			del xVector[classNameIndex-1]
			xVector = [float(x) for x in xVector]

			lloyd.addTrainingVector(xVector)

		return lloyd
	except:
		print("Error al leer el fichero")

''' This method loads SOM needed values and adds the to the wrapper class SOM '''

def loadFileSOM(file,classNameIndex):
	
	som = SOM(N = constants.getN(),maxK = constants.getSOMMaxK(),tolerance = constants.getSOMTolerance(),Tdistance = constants.getSOMDistanceT(),floatGamma = constants.getSOMGammaK(),alfaInicial = constants.getSOMInitialAlfa(),alfaFinal = constants.getSOMFinalAlfa(),variableGamma = False)
	#centers
	som.addInitialCenter([4.6,3.0,4.0,0.0],"Iris-setosa")
	som.addInitialCenter([6.8,3.4,4.6,0.7],"Iris-versicolor")
	fileHelper = FileHelper()

	try:
		f = fileHelper.openReadOnlyFile(file)
		
		lineas = f.readlines()
		xVector = []

		for linea in lineas:

			xVector = linea.strip("\r\n").split(",")
			del xVector[classNameIndex-1]
			xVector = [float(x) for x in xVector]

			som.addTrainingVector(xVector)

		return som
	except:
		print("Error al leer el fichero")

def loadFileTest(file,classNameIndex):
	
	fileHelper = FileHelper()
	try:
		f = fileHelper.openReadOnlyFile(file)
		
		lineas = f.readlines()
		xVector = []

		for linea in lineas:

			xVector = linea.strip("\r\n").split(",")
			del xVector[classNameIndex-1]
			xVector = [float(x) for x in xVector]

		return xVector
	except:
		print("Error al leer el fichero")



if __name__ == "__main__":
	

	test1 = loadFileTest("TestIris01.txt",5)
	print "Loaded test ", test1
	test2 = loadFileTest("TestIris02.txt",5)
	print "Loaded test ", test2
	test3 = loadFileTest("TestIris03.txt",5)
	print "Loaded test ", test3

	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++"
	print "+++++++++++                KMEANS"
	print "+++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"

	k = loadFileKMeans("Iris2Clases.txt",5)

	print ">>> Carga finalizada KMEANS"

	k.doTraining(epsilonLimit=constants.getKMeansEpsilon(),b=constants.getKMeansB())

	print "\n>>> Test KMEANS \n"
	print "Test 1:"
	print  k.clasifyEuclideanDistance(test1),"\n"
	print k.clasifyProbability(test1,constants.getKMeansB())
	print "\nTest 2:"
	print k.clasifyEuclideanDistance(test2),"\n"
	print k.clasifyProbability(test2,constants.getKMeansB())
	print "\nTest 3:"
	print  k.clasifyEuclideanDistance(test3),"\n"
	print k.clasifyProbability(test3,constants.getKMeansB())
	
	
	print "\n\n\n"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++"
	print "+++++++++++                BAYES"
	print "+++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"

	bayes = loadFileBayes("Iris2Clases.txt",5)

	print ">>> Carga finalizada BAYES"
	bayes.doTraining()
	classes = bayes.getClasses()
	for value in classes:
		print "\n>>>>>>>>> Clase: ", value
		print "\n>>> M:\n", bayes.getClass(value).getMVector()
		print "\n>>> C:\n", bayes.getClass(value).getCMatrix()
	print "\n>>> Test Bayes \n"
	print "Test 1:"
	print test1," clasificado como clase ", bayes.clasify(test1)
	print "\nTest 2:"
	print test2," clasificado como clase ", bayes.clasify(test2)
	print "\nTest 3:"
	print test3," clasificado como clase ", bayes.clasify(test3)

	print "\n\n\n"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++"
	print "+++++++++++                LLOYD"
	print "+++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"

	lloyd = loadFileLloyd("Iris2Clases.txt",5)

	print ">>> Carga finalizada LLOYD"
	lloyd.generateTraining()
	print ">>> Valores de los centros"
	print lloyd.getCenters()
	print "\n>>> Test Lloyd \n"
	print "Test 1:"
	print test1," clasificado como clase ", lloyd.clasify(test1)
	print "\nTest 2:"
	print test2," clasificado como clase ", lloyd.clasify(test2)
	print "\nTest 3:"
	print test3," clasificado como clase ", lloyd.clasify(test3)

	print "\n\n\n"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++"
	print "+++++++++++                SOM"
	print "+++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"
	print "++++++++++++++++++++++++++++++++++++++++++++"

	som = loadFileSOM("Iris2Clases.txt",5)
	print ">>> Carga finalizada SOM"

	som.doTraining()
	print ">>> Valores de los centros"
	print som.getCenters()
	print "\n>>> Test SOM \n"
	print "Test 1:"
	print test1," clasificado como clase ", som.clasify(test1)
	print "\nTest 2:"
	print test2," clasificado como clase ", som.clasify(test2)
	print "\nTest 3:"
	print test3," clasificado como clase ", som.clasify(test3)