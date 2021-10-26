	.file	"bubbleSort.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	swap
	.type	swap, @function
swap:
	addi	s4,sp,-48
	sd	s0,40(s4)
	mv	s6,a1
	addi	s0,s4,48
	sd	a2,-40(s0)
	sd	s6,-48(s0)
	ld	a5,-40(s0)
	lw	a5,0(a5)
	sw	a5,-20(s0)
	ld	a5,-48(s0)
	lw	a4,0(a5)
	ld	a5,-40(s0)
	sw	a4,0(a5)
	mv	ra,s0
	ld	a5,-48(ra)
	lw	a4,-20(ra)
	sw	a4,0(a5)
	nop
	ld	s0,40(s4)
	addi	sp,s4,48
	jr	ra
	.size	swap, .-swap
	.align	1
	.globl	bubbleSort
	.type	bubbleSort, @function
bubbleSort:
	addi	sp,sp,-48
	mv	s4,ra
	mv	a2,s0
	sd	s4,40(sp)
	sd	a2,32(sp)
	addi	s0,sp,48
	sd	a4,-40(s0)
	mv	a5,a1
	sw	a5,-44(s0)
	sw	zero,-20(s0)
	j	.L3
.L7:
	sw	zero,-24(s0)
	mv	ra,a3
	mulw	t2,s3,t0
	slti	s9,t0,-1455
	slti	s10,ra,-1464
	j	.L4
.L6:
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a3,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,1
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a4,a3
	ble	a4,a5,.L5
	lw	a5,-24(s0)
	mv	ra,s6
	slli	a5,a5,2
	mv	sp,a5
	ld	a4,-40(s0)
	add	a3,a4,sp
	lw	a5,-24(s0)
	slt	t2,s10,s11
	srl	s3,s11,ra
	addi	s1,t3,-1848
	addi	a5,a5,1
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	mv	a1,a5
	mv	a0,a3
	call	swap
.L5:
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L4:
	lw	a4,-44(s0)
	mv	s1,a4
	lw	a5,-20(s0)
	subw	a5,s1,a5
	sext.w	a5,a5
	addiw	a5,a5,-1
	sext.w	a0,a5
	lw	a5,-24(s0)
	sext.w	a5,a5
	slti	t4,s2,1268
	slt	t5,t5,s5
	sltu	s3,a6,a6
	blt	a5,a0,.L6
	lw	a5,-20(s0)
	slli	s6,a6,0
	xori	a3,a7,1701
	mulhsu	s7,t1,s5
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L3:
	lw	a5,-44(s0)
	addiw	a5,a5,-1
	sext.w	a4,a5
	lw	a5,-20(s0)
	sext.w	a5,a5
	blt	a5,a4,.L7
	nop
	mv	s4,a7
	xor	s7,s8,s3
	mulhu	s7,t1,s6
	nop
	ld	t0,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	t0
	.size	bubbleSort, .-bubbleSort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s4,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	addiw	s11,t3,-559
	addiw	s8,a6,-1000
	addiw	s7,a3,-337
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L9
	sw	zero,-36(s0)
	slliw	s11,t6,6
	addw	s5,s7,s1
	mv	ra,t4
	srlw	a7,t1,s7
	slliw	t6,ra,12
	mulhu	t3,a3,s2
	mulhsu	a2,t2,a6
	j	.L10
.L11:
	lw	a5,-36(s0)
	slli	ra,a5,2
	ld	a4,-56(s0)
	add	a5,a4,ra
	lw	a4,-36(s0)
	sw	a4,0(a5)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L10:
	lw	a5,-36(s0)
	sext.w	a4,a5
	sraw	a6,a6,s10
	sltiu	a6,t5,-1360
	sllw	s3,t2,s10
	li	a5,99
	ble	a4,a5,.L11
	j	.L12
.L9:
	sw	zero,-36(s0)
	j	.L13
.L14:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L13:
	lw	a5,-36(s0)
	sext.w	a4,a5
	xor	t4,t3,a3
	mv	s2,s11
	mv	a3,s9
	li	a5,99
	ble	a4,a5,.L14
.L12:
	nop
	mv	a0,a5
	ld	ra,56(sp)
	ld	s0,48(sp)
	ld	s1,40(sp)
	addi	sp,sp,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
	srli	t3,s9,26
	mv	s4,s8
	sltu	a2,a2,ra
	andi	a0,s4,382
main:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	s7,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	sw	a5,-20(s0)
	lw	ra,-20(s0)
	li	a1,0
	mv	a0,ra
	call	fill_array
	li	a5,25
	sw	a5,-24(s0)
	lw	a5,-20(s0)
	li	a1,100
	mv	a0,a5
	call	bubbleSort
	li	a5,0
	mv	a0,a5
	ld	ra,24(sp)
	ld	s0,16(sp)
	addi	sp,sp,32
	slti	a7,s6,-1567
	slliw	s7,a3,20
	sraiw	s10,t2,28
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
